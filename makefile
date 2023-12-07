CC=python3
INSTALLER=pip
TOOLS=ffmpeg
PLAT=win-amd64
SERVERS=ShuaigaoDiscord/src/servers

install:
	$(CC) -m $(INSTALLER) install --upgrade pip
	$(INSTALLER) install --upgrade setuptools wheel
	sudo apt update && sudo apt upgrade
	
	$(INSTALLER) install -r ./requirements.txt 
	sudo apt install $(TOOLS)
uninstall:
	$(INSTALLER) uninstall $(MODULES)

test_resources:
	$(CC) ./tests/test_resources.py

clean:
	rm -rf ./src/tests
	find ./logs -type d -name "__pycache__" -exec rm -rf {} \;
	find ./scripts -type d -name "__pycache__" -exec rm -rf {} \;
	find ./src -type d -name "__pycache__" -exec rm -rf {} \;
	find ./tests -type d -name "__pycache__" -exec rm -rf {} \;
	find ./logs -type f -name "*.log" -exec rm -rf {} \;
	clear||cls