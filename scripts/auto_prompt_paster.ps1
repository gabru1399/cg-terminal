# scripts/auto_prompt_paster.ps1
# Automates pasting the canonical invocation prompt into Antigravity and hitting Enter

param (
    [int]$IntervalSeconds = 1200 # 20 minutes
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

$promptPath = "desk/CANONICAL_PROMPT.txt"

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
    if (-not (Test-Path $promptPath)) {
        Write-Warning "Prompt file $promptPath not found!"
        return
    }
    $promptText = Get-Content $promptPath -Raw

    # 1. Set Windows Clipboard
    Set-Clipboard -Value $promptText
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Canonical prompt copied to clipboard."

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

        # 3. Paste and Send Enter
        [System.Windows.Forms.SendKeys]::SendWait("^v")
        Start-Sleep -Milliseconds 300
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Successfully pasted prompt and hit ENTER into Antigravity!"
    } else {
        Write-Warning "Could not find Antigravity window. Please ensure Antigravity IDE is open on your desktop."
    }
}

Write-Host "=========================================================="
Write-Host "Antigravity Autonomous Prompt Paster Initialized"
Write-Host "Interval: $IntervalSeconds seconds"
Write-Host "Source: $promptPath"
Write-Host "=========================================================="

while ($true) {
    Send-PromptToAntigravity
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sleeping for $IntervalSeconds seconds until next round..."
    Start-Sleep -Seconds $IntervalSeconds
}
