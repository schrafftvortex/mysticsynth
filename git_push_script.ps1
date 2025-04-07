# Navigate to your repository
Set-Location "C:\Users\Regis\mysticsynth"

# Prompt for a commit message with a popup box
Add-Type -AssemblyName Microsoft.VisualBasic
$commitMessage = [Microsoft.VisualBasic.Interaction]::InputBox('Enter your commit message:', 'Git Commit Message')

# Exit if no message provided
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    [System.Windows.Forms.MessageBox]::Show('Commit canceled. No message provided.', 'Canceled', 'OK', 'Information')
    exit
}

# Run git commands
git add .
git commit -m "$commitMessage"
git push origin main

# Notify completion
[System.Windows.Forms.MessageBox]::Show('Your changes have been pushed!', 'Success', 'OK', 'Information')
