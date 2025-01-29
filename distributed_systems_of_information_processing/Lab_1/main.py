class Process:
    def __init__(self, id):
        self.id = id
        self.left_process = None
        self.right_process = None

    def set_left(self, left_process):
        self.left_process = left_process

    def set_right(self, right_process):
        self.right_process = right_process

    def __str__(self):
        return f'Process {self.id}: left_process_id={self.left_process.id}, right_process_id={self.right_process.id}'

    def send_to_left(self, data):
        print(f'Process {self.id} sent to left neighbour process with id {self.left_process.id} message: {data}')
        self.left_process.receive_message(self.id, data)

    def send_to_right(self, data):
        print(f'Process {self.id} sent to right neighbour process with id {self.right_process.id} message: {data}')
        self.right_process.receive_message(self.id, data)

    def receive_message(self, sender_id, data):
        print(f'Process {self.id} received message from process {sender_id} message: {data}')
        # TODO: impl


class HSElectionDemo:
    def __init__(self, proceses_count=4):
        if proceses_count <= 1:
            raise ValueError('Process count must be greater than 1')

        self.processes_count = proceses_count
        self.__init_processes()

    def __init_processes(self):
        self.processes = []

        for i in range(self.processes_count):
            self.processes.append(Process(i))

        for i in range(self.processes_count):
            current_process = self.processes[i]
            left_process_idx = i - 1 if i != 0 else self.processes_count - 1
            right_process_idx = i + 1 if i != self.processes_count - 1 else 0

            current_process.set_left(self.processes[left_process_idx])
            current_process.set_right(self.processes[right_process_idx])

    def start_election(self):
        print('Election started')
        for p in self.processes:
            print(p)


def main():
    processes_count = 4
    demo = HSElectionDemo(processes_count)
    demo.start_election()


if __name__ == "__main__":
    main()