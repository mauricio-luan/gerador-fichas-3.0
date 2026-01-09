import unittest
import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from schemas.responses import Customer, Data, CustomFields
from logic.monta_ficha import monta_ficha


class TestMontaFicha(unittest.TestCase):
    def test_monta_ficha_criacao_sucesso(self):
        """
        Testa se a ficha é criada corretamente com dados válidos.
        """
        customer_data = Customer(
            success=True,
            data=[
                Data(
                    name="EMPRESA TESTE LTDA",
                    internal_id="00001-00002-00003",
                    custom_fields=[
                        CustomFields(name="Nome Fantasia", value="Fantasia Teste"),
                        CustomFields(name="CNPJ", value="12.345.678/0001-99"),
                        CustomFields(name="Endereco", value="Rua das Flores"),
                        CustomFields(name="Numero", value="123"),
                        CustomFields(name="Bairro", value="Centro"),
                        CustomFields(name="Cidade", value="Porto Alegre"),
                        CustomFields(name="UF", value="RS"),
                        CustomFields(name="COMERCIAL - Contato", value="João Silva"),
                        CustomFields(
                            name="COMERCIAL - Telefone", value="51 99999-9999"
                        ),
                        CustomFields(name="COMERCIAL - E-mail", value="joao@teste.com"),
                    ],
                )
            ],
        )

        protocol = 12345
        n_terminais = 2
        servico_cartao = "SCS_VERO"

        ficha = monta_ficha(protocol, customer_data, n_terminais, servico_cartao)

        self.assertEqual(ficha.razao_social, "EMPRESA TESTE LTDA")
        self.assertEqual(ficha.nome_fantasia, "Fantasia Teste")
        self.assertEqual(ficha.cnpj, "12.345.678/0001-99")
        self.assertEqual(ficha.endereco, "RUA DAS FLORES, 123")  # Espera uppercase
        self.assertEqual(ficha.servico_cartao, "SCS_VERO")

        hoje = date.today().strftime("%d/%m/%Y")
        self.assertEqual(ficha.chamado, f"12345 - {hoje}")

        esperado_token = "000020000301 | 000020000302"
        self.assertEqual(ficha.token, esperado_token)


if __name__ == "__main__":
    unittest.main()
