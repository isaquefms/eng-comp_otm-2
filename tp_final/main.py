"""
    Simulação de uma fila Markoviana. Nesse processo iremos simular uma sistema de atendimento ao usuário para emissão
    senhas para atendimento.

    Dessa forma, o problema possui como característica uma fila FIFO que recebe clientes para emissão de senhas de
    atendimento. O primeiro cliente da fila é atendido pelo mecanismo de atendimento eletrónico que emite uma senha de
    acordo com a necessidade de atendimento do usuário. Sendo assim, o mecanismo de atendimento suporta apenas um
    usuário por vez.

    Um sistema M/M/s foi modelado para esse problema tendo como base um minuto como unidade de tempo. Sendo assim, temos
    lambda igual a 1 e mi igual a 2, ou seja, temos a chegada de 1 cliente em média a cada um minuto e o atendimento de
     2 clientes por minuto em média. 1/lambda = 1/1 e 1/mi = 1/2.

    Modelos:
        - Fila: Modelo da fila que recebe um usuário e o insere na posição devida.
        - Mecanismo de atendimento: Modelo que recebendo um usuário executa a ação de atendimento.
        - Sistema de filas: Interação entre a Fila e o Mecanismo de Atendimento.
"""
import itertools
from typing import List

import numpy

# Constantes
LAMBDA = 2
MI = 1
ALPHA = 1/LAMBDA
BETA = 1/MI


class Client:
    """Classe para representar o objeto cliente.
    """

    new_id = itertools.count()

    def __init__(self):
        self._hold_time = 0
        self._id = next(Client.new_id)

    def increment_hold_time(self) -> None:
        self._hold_time += 1

    def get_hold_time(self) -> int:
        return self._hold_time

    def __str__(self) -> str:
        return f'Cliente: {self._id}'


class Queue:
    """Classe para representação da fila.
    """

    def __init__(self):
        self._queue = None
        self._queue_length = None

    def queue_length_register(self) -> None:
        if self._queue_length is None:
            self._queue_length = []
        self._queue_length.append(len(self._queue))

    def get_mean_queue_length(self) -> None:
        return sum(self._queue_length)/len(self._queue_length)

    def populate_queue(self, client_length: int) -> None:
        """Realiza o preenchimento da fila.

        Args:
            client_length: Quantidade de clientes a se adicionar.

        Returns: None.
        """
        if self._queue is None:
            self._queue = []
        # inserimos os novos clientes a fila
        for _ in range(client_length):
            new_client = Client()
            self._queue.append(new_client)
        # registro do tamanho atual da fila
        self.queue_length_register()

    def get_next_clients(self, served_client_len: int) -> List[Client]:
        """Obtém os próximos elementos da fila.

        Returns: Elemento retornado.
        """
        clients = []
        for _ in range(served_client_len):
            try:
                clients.append(self._queue.pop(0))
            except IndexError:
                break
        return clients

    def print_queue(self) -> None:
        """Imprime a fila.

        Returns: None.
        """
        print('Fila: ', end=' ')
        for element in self._queue:
            print(element, end='\t')
        print()

    def add_queue_hold_time(self) -> None:
        for i, _ in enumerate(self._queue):
            self._queue[i].increment_hold_time()


class ServiceMechanism:
    """Classe para representar o mecanismo de atendimento.
    """

    def __init__(self):
        self._clients_served = None

    def serve_next_clients(self, clients: List[Client]) -> None:
        """Insere na fila de atendimento os clientes atendidos.

        Args:
            clients: Cliente que está sendo atendido.

        Returns: None.
        """
        if self._clients_served is None:
            self._clients_served = []
        for client in clients:
            self._clients_served.append(client)

    def get_clients_served_length(self) -> int:
        return len(self._clients_served)

    def print_clients_served(self) -> None:
        print('Clientes atendidos: ', end=' ')
        for client in self._clients_served:
            print(client, end='\t')
        print()

    def get_hold_total_time(self) -> int:
        return sum(served_client.get_hold_time() for served_client in self._clients_served)


class QueueSystem:
    """Representação do Sistema de filas.
    """

    def __init__(self, t: int):
        self._t = t
        self._queue = Queue()
        self._service_mechanism = ServiceMechanism()

    def exponential_distribution(self, scale: float) -> List[int]:
        elements = numpy.random.exponential(scale, self._t)
        elements = [int(element) for element in elements]
        return elements

    def simulate_system(self) -> None:
        clients_arrived = self.exponential_distribution(ALPHA)
        clients_served = self.exponential_distribution(BETA)
        for clients_arrived_len, clients_served_len in zip(clients_arrived, clients_served):
            self._queue.populate_queue(clients_arrived_len)
            next_clients = self._queue.get_next_clients(clients_served_len)
            self._service_mechanism.serve_next_clients(next_clients)
            self._queue.add_queue_hold_time()

    def print_simulation_info(self) -> None:
        print('----------------------')
        print(f'Duração da simulação: {self._t} minutos')
        print(f'Número de clientes atendidos/Número de Tarefas'
              f' realizadas: {self._service_mechanism.get_clients_served_length()}')
        print(f'Duração média de uma tarefa: {round(self._t/self._service_mechanism.get_clients_served_length(), 2)} '
              f'minutos')
        print(f'Tempo médio de espera médio de '
              f'uma tarefa: {round(self._service_mechanism.get_hold_total_time()/self._service_mechanism.get_clients_served_length(), 2)} minutos')
        total_time = self._t + self._service_mechanism.get_hold_total_time()
        print(f'Tempo total médio de uma tarefa: {round(total_time/self._service_mechanism.get_clients_served_length(), 2)} minutos')
        print(f'Tamanho médio da fila: {self._queue.get_mean_queue_length()}')


if __name__ == '__main__':
    qs = QueueSystem(1000)
    qs.simulate_system()
    qs.print_simulation_info()
