# Senior Project Manager

## Description:
A web-based application that students and advisors can use to share project ideas,

communicate with each other, and to form teams with an assigned advisor.

### Members:
- Pedro Elizondo (pedro.elizondo02@utrgv.edu)
- Angelo Brian Navilon (angelobrian.navilon01@utrgv.edu)
- Angel Ballesteros (angel.ballesteros01@utrgv.edu)
- Alejandro Garcia (alejandro.garcia35@utrgv.edu)

### Advisor: 
Dr. Jonathan Reyes (jonatan.reyes01@utrgv.edu)

### Codespace Setup Instructions
```sh
chmod u+x codespace_setup.sh
./codespace_setup.sh
```
Then:
```sh
chmod u+x codespace_activate.sh
./codespace_activate.sh
```
### Making a Seperate Branch from Main (Group Members Only)
Step 1: Ensure Local Repo is Up to Date
```sh
git checkout main       # Switch to the main branch
git pull origin main    # Get the latest changes from GitHub
```
Step 2: Create and Switch to the New Branch
```sh
git checkout -b feature-branch-name   # "feature" would be what you are implementing
```
Step 3: Make your changes and commit
```sh
git add .      # Stage all changed files
git commit -m "Your commit message here"
```
Step 4: Push the Branch into Github
```sh
git push origin feature-branch-name
```
Step 5: Create a Pull Request

Go to your repository on GitHub.
Click on the "Compare & pull request" button that appears after pushing the branch.
Add a clear title and description for your changes.
Select main as the base branch and your new branch as the compare branch.
Click Create pull request.

Step 6: Request Reviews and Merge

If necessary, request a review from teammates or an advisor.
Once approved, merge the pull request.
After merging, delete the feature branch on GitHub.

Step 7: Clean Up Locally
```sh
git checkout main            # Switch back to main
git pull origin main         # Get the latest changes
git branch -d feature-branch-name  # Delete the local branch
```
