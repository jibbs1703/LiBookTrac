# Default commit message
COMMIT_MSG ?= "refactored user models and updated project requirements and description"

# Target to add changes to staging
add:
	   git add .

# Target to commit with a message
commit: add
	    git commit -m $(COMMIT_MSG)

# Target to push to the default branch
push: commit
	     git push

# Run all targets
all: push
