import pandas as pd

#informações basicas de uma pessoa
class Pessoa:
    def __init__(self, nome, idade, email):
        self.nome = nome
        self.idade = idade
        self.email = email

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}, Idade: {self.idade}, Email: {self.email}")

#informações extras pessoa para cliente
class Cliente(Pessoa):
    def __init__(self, nome, idade, email, cpf):
        super().__init__(nome, idade, email)
        self.cpf = cpf

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print(f"CPF: {self.cpf}")

#informações extras pessoa para funcionario
class Funcionario(Pessoa):
    def __init__(self, nome, idade, email, cargo):
        super().__init__(nome, idade, email)
        self.cargo = cargo

    def exibir_informacoes(self):
        super().exibir_informacoes()
        print(f"Cargo: {self.cargo}")

#define capacidade, preço e ocupação do quarto
class Quarto:
    def __init__(self, numero, capacidade, preco_diaria, nome):
        self.numero = numero
        self.capacidade = capacidade
        self.preco_diaria = preco_diaria
        self.nome = nome
        self.ocupado = False

    def ocupar_quarto(self):
        self.ocupado = True

    def desocupar_quarto(self):
        self.ocupado = False

    def esta_ocupado(self):
        return self.ocupado

#para reservar o quarto
class Reserva:
    def __init__(self, cliente, quarto, data_inicio, data_fim, cpf):
        self.cliente = cliente
        self.quarto = quarto
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.checkout_realizado = False
        self.cpf = cpf

#exibe as informações quando o checkout é realizado
    def realizar_checkout(self, cpf):
        if not self.checkout_realizado and self.cpf == cpf:
            fatura = Fatura(self)
            fatura.calcular_valor_total()
            fatura.exibir_fatura()
            self.checkout_realizado = True
            print("Checkout realizado com sucesso.")
        else:
            print("Reserva não encontrada ou já realizou checkout.")

#calcula o valor da estadia de acordo com o periodo da reserva
class Fatura:
    def __init__(self, reserva):
        self.reserva = reserva
        self.valor_total = 0

    def calcular_valor_total(self):
        dias = (pd.to_datetime(self.reserva.data_fim, format='%d-%m-%Y') -
                pd.to_datetime(self.reserva.data_inicio, format='%d-%m-%Y')).days
        self.valor_total = dias * self.reserva.quarto.preco_diaria

    def exibir_fatura(self):
        print(f"Fatura para {self.reserva.cliente.nome}")
        print(f"Quarto: {self.reserva.quarto.nome}")
        print(f"Data de Início: {self.reserva.data_inicio}, Data de Fim: {self.reserva.data_fim}")
        print(f"Valor Total: R$ {self.valor_total:.2f}")

#o cliente consegue avaliar os serviços do hotel
class AvaliacaoServico:
    def __init__(self, reserva, nota_atendimento, nota_limpeza, nota_conforto):
        self.reserva = reserva
        self.nota_atendimento = nota_atendimento
        self.nota_limpeza = nota_limpeza
        self.nota_conforto = nota_conforto

    def exibir_avaliacao(self):
        print(f"Avaliação para Reserva do cliente {self.reserva.cliente.nome}:")
        print(f"Nota Atendimento: {self.nota_atendimento}")
        print(f"Nota Limpeza: {self.nota_limpeza}")
        print(f"Nota Conforto: {self.nota_conforto}")

#para criar eventos que acontecerão nas instalaçoes do hotel
class EventoHotel:
    def __init__(self, nome, data, descricao):
        self.nome = nome
        self.data = data
        self.descricao = descricao

    def exibir_informacoes(self):
        print(f"Evento: {self.nome}")
        print(f"Data: {self.data}")
        print(f"Descrição: {self.descricao}")

#para datar os pagamentos e salvá-los em arquivo ou caso queira poderá exibi-los na tela
class HistoricoPagamentos:
    def __init__(self):
        self.pagamentos = []
        self.filename_pagamentos = "pagamentos.csv"
        self.carregar_pagamentos()

    def carregar_pagamentos(self):
        try:
            df_pagamentos = pd.read_csv(self.filename_pagamentos)
            for _, row in df_pagamentos.iterrows():
                pagamento = {
                    'Cliente': row['Cliente'],
                    'Valor': row['Valor'],
                    'Data': row['Data'],
                }
                self.pagamentos.append(pagamento)
        except FileNotFoundError:
            pass

    def exportar_pagamentos_csv(self):
        df_pagamentos = pd.DataFrame(self.pagamentos)
        df_pagamentos.to_csv(self.filename_pagamentos, index=False)

    def adicionar_pagamento(self, cliente, valor, data):
        pagamento = {
            'Cliente': cliente,
            'Valor': valor,
            'Data': data,
        }
        self.pagamentos.append(pagamento)
        self.exportar_pagamentos_csv()

    def exibir_pagamentos(self):
        for pagamento in self.pagamentos:
            print(f"Cliente: {pagamento['Cliente']}, Valor: R$ {pagamento['Valor']:.2f}, Data: {pagamento['Data']}")

#classe controladora do programa
class Hotel:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.funcionarios = []
        self.quartos = self.criar_quartos_fixos()
        self.reservas = []
        self.eventos = []
        self.filename_reservas = "reservas.csv"
        self.filename_clientes = "clientes.csv"
        self.filename_funcionarios = "funcionarios.csv"
        self.filename_eventos = "eventos.csv"
        self.carregar_clientes()
        self.carregar_reservas()
        self.carregar_funcionarios()
        self.carregar_eventos()
        self.historico_pagamentos = HistoricoPagamentos()

    #para checar os clientes que se cadastraram anteriormente
    def carregar_clientes(self):
        try:
            df_clientes = pd.read_csv(self.filename_clientes)
            for _, row in df_clientes.iterrows():
                if 'CPF' in df_clientes.columns:
                    cliente = Cliente(row['Nome'], row['Idade'], row['Email'], row['CPF'])
                else:
                    cliente = Pessoa(row['Nome'], row['Idade'], row['Email'])
                self.clientes.append(cliente)
        except FileNotFoundError:
            pass

    # para checar as reservas que foram feitas anteriormente
    def carregar_reservas(self):
        try:
            df_reservas = pd.read_csv(self.filename_reservas)
            for _, row in df_reservas.iterrows():
                cliente = next((c for c in self.clientes if isinstance(c, Cliente) and c.nome == row['Cliente']), None)
                quarto = next((q for q in self.quartos if q.nome == row['Quarto']), None)
                if cliente and quarto:
                    reserva = Reserva(cliente, quarto, row['Data Início'], row['Data Fim'], row['CPF'])
                    self.reservas.append(reserva)
        except FileNotFoundError:
            pass

    # para checar os funcionarios que foram cadastrados anteriormente
    def carregar_funcionarios(self):
        try:
            df_funcionarios = pd.read_csv(self.filename_funcionarios)
            for _, row in df_funcionarios.iterrows():
                funcionario = Funcionario(row['Nome'], row['Idade'], row['Email'], row['Cargo'])
                self.funcionarios.append(funcionario)
        except FileNotFoundError:
            pass

#salva todos clientes em um arquivo
    def exportar_clientes_csv(self):
        df_clientes = pd.DataFrame({
            'Nome': [cliente.nome for cliente in self.clientes],
            'Idade': [cliente.idade for cliente in self.clientes],
            'Email': [cliente.email for cliente in self.clientes],
            'CPF': [cliente.cpf for cliente in self.clientes] if isinstance(self.clientes[0], Cliente) else [""],
        })
        df_clientes.to_csv(self.filename_clientes, index=False)

    # salva todas as reservas em um arquivo
    def exportar_reservas_csv(self):
        df_reservas = pd.DataFrame({
            'Cliente': [reserva.cliente.nome for reserva in self.reservas],
            'Quarto': [reserva.quarto.nome for reserva in self.reservas],
            'Data Início': [reserva.data_inicio for reserva in self.reservas],
            'Data Fim': [reserva.data_fim for reserva in self.reservas],
            'CPF': [reserva.cpf for reserva in self.reservas],
        })
        df_reservas.to_csv(self.filename_reservas, index=False)

    # salva todos os funcionarios em um arquivo
    def exportar_funcionarios_csv(self):
        df_funcionarios = pd.DataFrame({
            'Nome': [funcionario.nome for funcionario in self.funcionarios],
            'Idade': [funcionario.idade for funcionario in self.funcionarios],
            'Email': [funcionario.email for funcionario in self.funcionarios],
            'Cargo': [funcionario.cargo for funcionario in self.funcionarios],
        })
        df_funcionarios.to_csv(self.filename_funcionarios, index=False)


    def criar_quartos_fixos(self):
        quartos = [
            Quarto(numero=1, capacidade=2, preco_diaria=100.0, nome="1"),
            Quarto(numero=2, capacidade=2, preco_diaria=100.0, nome="2"),
            Quarto(numero=3, capacidade=4, preco_diaria=100.0, nome="3"),
            Quarto(numero=4, capacidade=2, preco_diaria=100.0, nome="4"),
            Quarto(numero=5, capacidade=2, preco_diaria=100.0, nome="5"),
        ]
        return quartos

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.exportar_clientes_csv()

    def adicionar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)
        self.exportar_funcionarios_csv()

    #checa se o quarto esta ocupado ou reserva para o cpf digitado
    def fazer_reserva(self, cliente, quarto, data_inicio, data_fim):
        if quarto.esta_ocupado():
            print(f"Quarto {quarto.nome} já está ocupado para o período selecionado.")
        else:
            cpf = "123456789"
            reserva = Reserva(cliente, quarto, data_inicio, data_fim, cpf)
            quarto.ocupar_quarto()
            self.reservas.append(reserva)
            self.exportar_reservas_csv()
            print(f"Reserva realizada com sucesso para o Quarto {quarto.nome}.")

    def exibir_reservas(self):
        for reserva in self.reservas:
            print(f"Cliente: {reserva.cliente.nome}, "
                  f"Quarto: {reserva.quarto.nome}, "
                  f"Data de Início: {reserva.data_inicio}, Data de Fim: {reserva.data_fim}, "
                  f"CPF: {reserva.cpf}")


    def realizar_checkout(self, cpf):
        for reserva in self.reservas:
            if not reserva.checkout_realizado and reserva.cpf == cpf:
                reserva.realizar_checkout(cpf)
                # Atualizar o arquivo CSV após o checkout
                self.exportar_reservas_csv()
                return
        print("Reserva não encontrada ou já realizou checkout.")

    def remover_reserva(self, cliente_nome):
        reservas_cliente = [reserva for reserva in self.reservas if reserva.cliente.nome == cliente_nome]

        if not reservas_cliente:
            print(f"Não há reservas para o cliente {cliente_nome}.")
            return

        for reserva in reservas_cliente:
            print(f"Cliente: {reserva.cliente.nome}, "
                  f"Quarto: {reserva.quarto.nome}, "
                  f"Data de Início: {reserva.data_inicio}, Data de Fim: {reserva.data_fim}, "
                  f"CPF: {reserva.cpf}")

        quarto_nome = "Quarto 1"
        reserva_encontrada = next((reserva for reserva in reservas_cliente if reserva.quarto.nome == quarto_nome), None)

        if reserva_encontrada:
            self.reservas.remove(reserva_encontrada)
            reserva_encontrada.quarto.desocupar_quarto()
            self.exportar_reservas_csv()
            print("Reserva removida com sucesso.")
        else:
            print("Quarto não encontrado na reserva.")

    def adicionar_avaliacao(self, reserva):
        nota_atendimento = float(input("Digite a nota de atendimento (0 a 10): "))
        nota_limpeza = float(input("Digite a nota de limpeza (0 a 10): "))
        nota_conforto = float(input("Digite a nota de conforto (0 a 10): "))
        avaliacao = AvaliacaoServico(reserva, nota_atendimento, nota_limpeza, nota_conforto)
        avaliacao.exibir_avaliacao()

    def carregar_eventos(self):
        try:
            df_eventos = pd.read_csv(self.filename_eventos)
            for _, row in df_eventos.iterrows():
                evento = EventoHotel(row['Nome'], row['Data'], row['Descrição'])
                self.eventos.append(evento)
        except FileNotFoundError:
            pass

    def exportar_eventos_csv(self):
        df_eventos = pd.DataFrame({
            'Nome': [evento.nome for evento in self.eventos],
            'Data': [evento.data for evento in self.eventos],
            'Descrição': [evento.descricao for evento in self.eventos],
        })
        df_eventos.to_csv(self.filename_eventos, index=False)

    def adicionar_evento(self, evento):
        self.eventos.append(evento)
        self.exportar_eventos_csv()

    def exibir_eventos(self):
        for evento in self.eventos:
            evento.exibir_informacoes()

    def realizar_pagamento(self, cliente, valor, data):
        self.historico_pagamentos.adicionar_pagamento(cliente, valor, data)
        print("Pagamento realizado com sucesso.")

    def exibir_historico_pagamentos(self):
        self.historico_pagamentos.exibir_pagamentos()

