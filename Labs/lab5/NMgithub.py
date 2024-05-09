import git

try:
    rep_path = "/home/student/git/netman"
    repo = git.Repo(rep_path)
    git = git.Git(rep_path)
    repo.git.add(update=True)
    repo.index.commit("Changes detected and pushing to GitHub via NMgithub.py")
    origin = repo.remote('origin')
    origin.push()
except Exception as e:
    print(e)