brew update
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
source ~/.zshrc  # Reload the shell configuration

brew install pyenv-virtualenv
pyenv virtualenv 3.12.7 chanvenv-3.12.7 
pyenv local chanvenv-3.12.7 

brew install direnv
eval "$(direnv hook zsh)"  # or `bash` if you’re using Bash
source ~/.zshrc

echo 'layout python $(pyenv which python)' > .envrc
direnv allow

pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
