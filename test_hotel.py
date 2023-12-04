import pytest
from datetime import datetime
from classesTeste import Hotel, Cliente, Funcionario, Quarto

@pytest.fixture
def hotel():
    return Hotel("Hotel Bedroom Dreams")

def test_adicionar_cliente(hotel):
    cliente = Cliente("João", 30, "joao@email.com", "123456789")
    hotel.adicionar_cliente(cliente)
    assert cliente in hotel.clientes

def test_adicionar_funcionario(hotel):
    funcionario = Funcionario("Maria", 25, "maria@email.com", "Recepcionista")
    hotel.adicionar_funcionario(funcionario)
    assert funcionario in hotel.funcionarios

def test_fazer_reserva(hotel):
    quarto = Quarto(1, 2, 100.0, "Quarto 1")
    hotel.quartos = [quarto]
    cliente = Cliente("João", 30, "joao@email.com", "123456789")
    data_inicio = "01-01-2023"
    data_fim = "05-01-2023"
    hotel.fazer_reserva(cliente, quarto, data_inicio, data_fim)
    assert hotel.reservas
    assert quarto.esta_ocupado()

def test_remover_reserva():
    hotel = Hotel("Hotel Teste")
    cliente = Cliente("João", "30", "joao@email.com", "123456789")
    quarto = Quarto(101, 2, 150.0, "Quarto 1")
    hotel.fazer_reserva(cliente, quarto, "01-01-2023", "05-01-2023")
    hotel.remover_reserva("João")
    assert len(hotel.reservas) == 0
    assert not quarto.esta_ocupado()

def test_realizar_pagamento(hotel):
    cliente = "João"
    valor = 500.0
    data = datetime.now().strftime("%d-%m-%Y")
    hotel.realizar_pagamento(cliente, valor, data)
    assert hotel.historico_pagamentos.pagamentos

def test_exibir_reservas(hotel, capsys):
    quarto = Quarto(1, 2, 100.0, "Quarto 1")
    cliente = Cliente("João", 30, "joao@email.com", "123456789")
    data_inicio = "01-01-2023"
    data_fim = "05-01-2023"
    hotel.fazer_reserva(cliente, quarto, data_inicio, data_fim)
    hotel.exibir_reservas()
    captured = capsys.readouterr()
    assert "Cliente: João" in captured.out
    assert "Quarto: Quarto 1" in captured.out
