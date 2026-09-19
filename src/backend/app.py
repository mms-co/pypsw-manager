import os
import webview

from api_bridge import APIBridge


# Application info
APP_NAME = "Password Generator"
SIZE = WIDTH, HEIGHT = 450, 600


def main():
	# Initialise the bridge API
	api = APIBridge()
	# Normalise paths and create the window
	current_dir = os.path.dirname(os.path.abspath(__file__))
	frontend_path = os.path.abspath(os.path.join(current_dir, '../frontend/index.html'))
	webview.create_window(
		title=APP_NAME,
		url=frontend_path,
		js_api=api,
		width=WIDTH,
		height=HEIGHT,
		resizable=False
	)
	webview.start(debug=True)

if __name__ == "__main__":
	main()