"""
    Simulação de uma fila Markoviana. Nesse processo iremos simular uma sistema de atendimento ao usuário para emissão
    senhas para atendimento.

    Dessa forma, o problema possui como característica uma fila FIFO que recebe clientes para emissão de senhas de
    atendimento. O primeiro cliente da fila é atendido pelo mecanismo de atendimento eletrónico que emite uma senha de
    acordo com a necessidade de atendimento do usuário. Sendo assim, o mecanismo de atendimento suporta apenas um
    usuário por vez.

    Um sistema M/M/s foi modelado para esse problema tendo como base um minuto como unidade de tempo. Sendo assim, temos
    lambda igual a 2 e mi igual a 1, ou seja, temos a chegada de 2 clientes a cada um minuto e o atendimento de um
    cliente por minuto. 1/lambda = 1/2 e 1/mi = 1.

    Modelos:
        - Fila: Modelo da fila que recebe um usuário e o insere na posição devida.
        - Mecanismo de atendimento: Modelo que recebendo um usuário executa a ação de atendimento.
        - Sistema de filas: Interação entre a Fila e o Mecanismo de Atendimento.
"""
# Constantes
LAMBDA = 2
MI = 1


class Queue:
    """Classe para representação da fila.
    """

    def __init__(self):
        self._queue = None
        self._last_client = 0

    def populate_queue(self) -> None:
        """Realiza o preenchimento da fila.

        Returns: None.
        """
        if self._queue is None:
            self._queue = []
        # inserimos os dois novos clientes a fila
        for n in range(LAMBDA):
            self._queue.append(self._last_client + (n + 1))
        # adicionamos a variável client
        self._last_client += LAMBDA

    def get_next_client(self) -> int:
        """Obtém o próximo elemento da fila.

        Returns: Elemento retornado.
        """
        return self._queue.pop(0)

    def print_queue(self) -> None:
        """Imprime a fila.

        Returns: None.
        """
        print('Fila: ', end=' ')
        for element in self._queue:
            print(element, end='\t')
        print()

    def get_last_client(self) -> int:
        """Imprime o último cliente.

        Returns: Último cliente.
        """
        return self._last_client


class ServiceMechanism:
    """Classe para representar o mecanismo de atendimento.
    """

    def __init__(self):
        self._clients_served = None

    def set_next_client(self, client: int) -> None:
        """Insere na fila o próximo cliente.

        Args:
            client: Cliente que está sendo atendido.

        Returns: None.
        """
        if self._clients_served is None:
            self._clients_served = []
        self._clients_served.append(client)

    def get_clients_served_length(self) -> int:
        return len(self._clients_served)

    def print_clients_served(self) -> None:
        print('Clientes atendidos: ', end=' ')
        for client in self._clients_served:
            print(client, end='\t')
        print()


class QueueSystem:
    """Representação do Sistema de filas.
    """

    def __init__(self, t: int):
        self._t = t
        self._queue = Queue()
        self._service_mechanism = ServiceMechanism()

    def simulate_system(self) -> None:
        for _ in range(1, self._t + 1):
            self._queue.populate_queue()
            next_client = self._queue.get_next_client()
            self._service_mechanism.set_next_client(next_client)

    def print_simulation_info(self) -> None:
        print('----------------------')
        print(f'Duração da simulação: {self._t} minutos')
        print(f'Número de clientes atendidos: {self._service_mechanism.get_clients_served_length()}')


if __name__ == '__main__':
    qs = QueueSystem(1000)
    qs.simulate_system()
    qs.print_simulation_info()
