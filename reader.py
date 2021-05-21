import obd

# obd.logger.setLevel(obd.logging.DEBUG)

notImportantPids = [
    int('0', 16),
    int('1', 16),
    int('2', 16),
    int('03', 16),
    int('13', 16),
    int('1C', 16),
    int('20', 16),
    int('21', 16),
    int('40', 16),
]


def extractSupported(bits):
    print(type(bits))


def isCmdImportant(cmd):
    if cmd.mode == 1 and not(cmd.pid in notImportantPids):
        return True
    return False


class Reader:

    def connect(self):
        self.conn = obd.Async()

    def disconnect(self):
        self.conn.unwatch_all()

    def checkAvailable(self):
        supportedPids = []
        for command in self.conn.supported_commands:
            print(command)
            if isCmdImportant(command):
                supportedPids.append(command)
        return supportedPids

    def watch(self, supported, pid_handler, dtc_handler):
        # First Get DTC
        self.dtc_handler = dtc_handler
        self.conn.watch(obd.commands.GET_DTC, callback=self.unwatchDTC)

        # Then PIDs
        for command in supported:
            self.conn.watch(command,  callback=pid_handler)

    def unwatchDTC(self, r):
        self.dtc_handler(r)
        self.conn.unwatch(obd.commands.GET_DTC)

    def start(self):
        self.conn.start()

    def stop(self):
        self.conn.stop()
