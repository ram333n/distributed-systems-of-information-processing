import math
from enum import Enum

class Direction(Enum):
    LEFT = 1,
    RIGHT = 2

    def inverse(self):
        return self.LEFT if self.value == self.RIGHT else self.RIGHT

class Message:
    def __init__(self, data, direction, hops_count=1, ack_leader=False):
        self.data = data
        self.direction = direction
        self.hops_count = hops_count
        self.ack_leader = ack_leader

    def __str__(self):
        return f'Message[data={self.data}, direction={self.direction}, hops_count={self.hops_count}, ack_leader={self.ack_leader}]'

class Process:
    def __init__(self, id):
        self.id = id
        self.is_leader = False
        self.left_process = None
        self.right_process = None
        self.is_round_finished_from_left = False
        self.is_round_finished_from_right = False
        self.round = 0
        self.is_acknowledged_about_leader = False

    def set_left(self, left_process):
        self.left_process = left_process

    def set_right(self, right_process):
        self.right_process = right_process

    def __str__(self):
        return f'Process {self.id}: left_process_id={self.left_process.id}, right_process_id={self.right_process.id}'

    def send(self, data, hops_count, direction, ack_leader=False):
        if direction == Direction.LEFT:
            self.send_to_left(data, hops_count, ack_leader)
        else:
            self.send_to_right(data, hops_count, ack_leader)

    def send_to_left(self, data, hops_count, ack_leader=False):
        print(f'Process {self.id} sent to left neighbour process with id {self.left_process.id} message: {data} and hops_count: {hops_count}')
        self.left_process.receive_message(self.id, Message(data, Direction.LEFT, hops_count, ack_leader))

    def send_to_right(self, data, hops_count, ack_leader=False):
        print(f'Process {self.id} sent to right neighbour process with id {self.right_process.id} message: {data} and hops_count: {hops_count}')
        self.right_process.receive_message(self.id, Message(data, Direction.RIGHT, hops_count, ack_leader))

    def receive_message(self, sender_id, message):
        if self.is_acknowledged_about_leader:
            return

        print(f'Process {self.id} received message from process {sender_id} message: {message}')
        cur_hops_count = message.hops_count - 1

        if message.ack_leader:
            self.__handle_leader_acknowledgment(message.data, message.direction)
            return

        if cur_hops_count == 0:
            self.__handle_message_return(sender_id, message)
            return

        if message.data > self.id:
            self.send(message.data, cur_hops_count, message.direction)
        elif message.data == self.id:
            self.is_leader = True
            print(f'Process {self.id} becomes the leader!')
            self.__notify_about_leader()

    def __handle_leader_acknowledgment(self, leader_id, direction):
        print(f'Process {self.id} received acknowledgment that process {leader_id} is leader!')
        self.is_acknowledged_about_leader = True
        self.send(leader_id, 1, direction, True)


    def __handle_message_return(self, sender_id, message):
        if message.data == self.id:
            if message.direction == Direction.LEFT:
                self.is_round_finished_from_right = True
            else:
                self.is_round_finished_from_left = True

            if self.is_round_finished_from_left and self.is_round_finished_from_right:
                self.round += 1
                print(f'Process {self.id} moves to the next round: {self.round}')

                self.send_to_left(self.id, 2 ** self.round)
                self.send_to_right(self.id, 2 ** self.round)

        else:
            self.send(message.data, 1, message.direction)

    def __notify_about_leader(self):
        self.send_to_left(self.id, 1 , True)
        self.send_to_right(self.id, 1 , True)


class HSElectionDemo:
    def __init__(self, processes_count=4):
        if processes_count <= 1:
            raise ValueError('Process count must be greater than 1')

        self.processes_count = processes_count
        self.__init_processes()

    def __init_processes(self):
        self.processes = []

        for i in range(self.processes_count):
            self.processes.append(Process(i))

        for i in range(self.processes_count):
            current_process = self.processes[i]
            left_process_idx = (i - 1) % self.processes_count
            right_process_idx = (i + 1) % self.processes_count

            current_process.set_left(self.processes[left_process_idx])
            current_process.set_right(self.processes[right_process_idx])

    def start_election(self):
        self.__print_processes()
        print(f'=====================Election started. Process count: {self.processes_count}=====================')

        init_hops_count = 1
        for process in self.processes:
            process.send_to_left(process.id, init_hops_count)
            process.send_to_right(process.id, init_hops_count)

    def __print_processes(self):
        print('=====================Processes=====================')
        for process in self.processes:
            print(process)


def main():
    processes_count = 4
    demo = HSElectionDemo(processes_count)
    demo.start_election()


if __name__ == "__main__":
    main()