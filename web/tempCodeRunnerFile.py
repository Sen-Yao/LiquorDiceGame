def start_server(start_fn, host, port):
    app = QApplication(sys.argv)

    window = Server(start_fn, host, port)
    window.show()

    sys.exit(app.exec())