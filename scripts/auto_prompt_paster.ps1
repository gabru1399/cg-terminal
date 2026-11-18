# scripts/auto_prompt_paster.ps1
# Automates pasting whatever is ALREADY copied in your Windows Clipboard into Antigravity and hitting Enter

param (
    [int]$IntervalSeconds = 1200 # 20 minutes (default)
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  using System.Text;

  public class Win32 {
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
  }
"@

function Get-AntigravityWindow {
    $targetHwnd = [IntPtr]::Zero
    $callback = [Win32+EnumWindowsProc]{
        param($hwnd, $lParam)
        if ([Win32]::IsWindowVisible($hwnd)) {
            $sb = New-Object System.Text.StringBuilder 256
            [void][Win32]::GetWindowText($hwnd, $sb, 256)
            $title = $sb.ToString()
            if ($title -like "*Antigravity*" -or $title -like "*cg-terminal*") {
                Set-Variable -Name targetHwnd -Value $hwnd -Scope 2
                return $false
            }
        }
        return $true
    }
    [Win32]::EnumWindows($callback, [IntPtr]::Zero)
    return $targetHwnd
}

function Send-PromptToAntigravity {
    # 1. Read existing Windows Clipboard without modifying it
    $clip = Get-Clipboard -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($clip)) {
        Write-Warning "[$(Get-Date -Format 'HH:mm:ss')] Clipboard is currently empty! Please copy your prompt first."
        return
    }

    $preview = if ($clip.Length -gt 70) { $clip.Substring(0, 70).Replace("`n", " ").Replace("`r", "") + "..." } else { $clip }
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Pasting copied clipboard: '$preview'"

    # 2. Locate Antigravity Window
    $hwnd = Get-AntigravityWindow
    if ($hwnd -eq [IntPtr]::Zero) {
        $p = Get-Process -Name "Antigravity" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
        if ($p) { $hwnd = $p.MainWindowHandle }
    }

    if ($hwnd -ne [IntPtr]::Zero) {
        [Win32]::ShowWindowAsync($hwnd, 9) # SW_RESTORE
        [Win32]::SetForegroundWindow($hwnd)
        Start-Sleep -Milliseconds 400

        # 3. Paste (Ctrl+V) and Send Enter
        [System.Windows.Forms.SendKeys]::SendWait("^v")
        Start-Sleep -Milliseconds 300
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Successfully pasted copied text and hit ENTER into Antigravity!"
    } else {
        Write-Warning "Could not find Antigravity window. Please ensure Antigravity IDE is open on your desktop."
    }
}

Write-Host "=========================================================="
Write-Host "Antigravity Pure-Clipboard Auto-Paster Active"
Write-Host "Interval: $IntervalSeconds seconds"
Write-Host "Behavior: Pastes whatever you have copied in Windows Clipboard"
Write-Host "=========================================================="

while ($true) {
    Send-PromptToAntigravity
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Next paste scheduled in $IntervalSeconds seconds (leave your prompt copied)..."
    Start-Sleep -Seconds $IntervalSeconds
}
