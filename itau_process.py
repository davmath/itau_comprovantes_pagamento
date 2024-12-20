from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

def login_itau():
    # Configuração do navegador (Chromedriver precisa estar no PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Abrir navegador e acessar a URL
        driver.get("https://www.itau.com.br/empresas")

        # 2. Clicar no botão "Mais Acessos"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='open_modal_more_access']"))
        ).click()

        # 3. Selecionar "Login One"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='id-more-access-select-login']/option[2]"))
        ).click()

        # 4. Inserir o usuário (dados fictícios)
        user_empresa = "123456789"  # Substituído por dados fictícios
        input_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='id-more-access-input-operator']"))
        )
        input_field.clear()
        input_field.send_keys(user_empresa)

        # 5. Clicar no botão "Avançar"
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='id-more-access-submit-button']"))
        ).click()

        # 6. Decodificar senha e clicar nos dígitos usando JavaScript
        password_empresa = "987654"  # Substituído por dados fictícios
        script = """
        // Define a senha
        var senha = "{password_empresa}";

        // Função para encontrar e clicar nos botões
        function clicarBotao(numero) {
            // Localiza todos os botões do teclado virtual
            var botoes = document.querySelectorAll('a.tecla');
            for (var botao of botoes) {
                // Verifica se o texto do botão contém o número desejado
                if (botao.innerText.includes(numero)) {
                    botao.click(); // Clica no botão
                    break; // Sai do loop após encontrar o botão correto
                }
            }
        }

        // Percorre cada dígito da senha e clica nos botões correspondentes
        for (var digito of senha) {
            clicarBotao(digito);
        }
        """.replace("{password_empresa}", password_empresa)
        driver.execute_script(script)

        # 7. Clicar no botão "Acessar"
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='acessar']"))
        ).click()

        # 8. Esperar pela tela principal
        WebDriverWait(driver, 80).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='rdBasico']"))
        )
        driver.find_element(By.XPATH, "//*[@id='rdBasico']").click()

        # 9. Continuar
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btn-continuar']"))
        ).click()

    except Exception as e:
        print(f"Erro durante o login: {e}")
    finally:
        # Fechar o navegador
        time.sleep(5)  # Apenas para visualização
        driver.quit()

def acesso_contas_pagar():
    # Configuração do navegador (Chromedriver precisa estar no PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Esperar pelo botão "contas a pagar"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='contas a pagar']"))
        )
        time.sleep(10)  # Adiciona um atraso após o carregamento

        # 2. Clicar no menu de usuário
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "user-menu-button"))
        ).click()

        # 3. Executar o script para acessar o Shadow DOM e listar as contas
        script = """
        // Função para acessar elementos dentro do Shadow DOM
        function getElementsInsideNestedShadowRoots(selectors, finalSelector) {
            let currentElement = document;
            for (const selector of selectors) {
                currentElement = currentElement.querySelector(selector);
                if (!currentElement) {
                    console.error(`Elemento com o seletor \"${selector}\" não encontrado.`);
                    return null;
                }
                if (currentElement.shadowRoot) {
                    currentElement = currentElement.shadowRoot;
                }
            }
            return currentElement.querySelectorAll(finalSelector);
        }

        // Seletores para acessar o Shadow DOM
        const selectors = [
            'chassi-root',
            'chassi-page-layout',
            'mat-side-nav-container > mat-side-nav:nth-of-type(2)',
            'chassi-switch-accounts-menu',
            'chassi-card-mf-wrapper',
            'mf-lista-contas',
            'app-main',
            'app-list-accounts',
            'section ul.ids-list'
        ];

        // Final selector para os elementos atualizados
        const finalSelector = 'li[id^=account-] > button > span > span.ids-list-item__sub-text > span:nth-child(2)';

        // Obter os elementos das contas
        const elements = getElementsInsideNestedShadowRoots(selectors, finalSelector);
        
        // Lista para armazenar os valores das contas
        let contentList = [];
        if (elements) {
            elements.forEach((el, index) => {
                const content = el.textContent.trim();
                // Captura o texto interno do elemento
                // Extrai apenas o valor após \"Conta e\" antes do traço com regex
                const match = content.match(/Contas\s+(\d+)/);
                if (match && match[1]) {
                    const accountNumber = match[1];
                    contentList.push(accountNumber);
                    console.log(`Elemento ${index}: ${accountNumber}`);
                } else {
                    console.warn(`Formato inesperado no elemento ${index}: ${content}`);
                }
            });
            console.log(`Total de elementos capturados: ${contentList.length}`);
        } else {
            console.error('Não foi possível encontrar os elementos.');
        }

        return contentList;
        """
        driver.execute_script(script)

        # 4. Clicar no botão "contas a pagar"
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='contas a pagar']"))
        ).click()

        # 5. Clicar no botão "comprovante"
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'comprovante')]"))
        ).click()

    except Exception as e:
        print(f"Erro durante o acesso: {e}")
    finally:
        # Fechar o navegador
        time.sleep(5)  # Apenas para visualização
        driver.quit()

def loop_comprovantes():
    # Configuração do navegador (Chromedriver precisa estar no PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Configurar lógica inicial para obter lista de contas
        lista_contas = []  # Simula a lógica anterior onde as contas foram carregadas
        if not lista_contas:
            print("Nenhuma conta encontrada.")
            return

        for conta in lista_contas:
            # 2. Esperar elemento de detalhes da conta
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='account-details']"))
            )

            # 3. Mudar para iframe relevante
            driver.switch_to.frame(driver.find_element(By.ID, "iframe-universal-single"))
            driver.switch_to.frame(driver.find_element(By.NAME, "CORPO"))

            # 4. Selecionar período
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='cboPeriodo']/option[8]"))
            ).click()

            # 5. Preencher datas
            dia_anterior, mes_anterior, ano_anterior = "01", "01", "2023"  # Exemplo

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_INI_DIA"))
            ).send_keys(dia_anterior)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_INI_MES"))
            ).send_keys(mes_anterior)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_INI_ANO"))
            ).send_keys(ano_anterior)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_FIN_DIA"))
            ).send_keys(dia_anterior)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_FIN_MES"))
            ).send_keys(mes_anterior)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "OP_FIN_ANO"))
            ).send_keys(ano_anterior)

            # 6. Clicar no botão de busca
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='buscar']"))
            ).click()

            # 7. Esperar por elemento final
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='chkTodos']"))
            )

            # 8. Selecionar todos e scrollar
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='chkTodos']"))
            ).click()

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 9. Fazer download de comprovantes
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='tbEmissao2']"))
            ).click()

            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='tbEmissao2']"))
            ).click()

            # 10. Controlar manipulação de janelas e imprimir comprovantes
            while len(driver.window_handles) < 2:
                time.sleep(2)

            driver.switch_to.window(driver.window_handles[-1])

            # Inserir código JavaScript para interações adicionais
            script = """
            // Função para acessar elementos dentro do Shadow DOM
            function getElementsInsideNestedShadowRoots(selectors) {
                let currentElement = document;
                for (const selector of selectors) {
                    currentElement = currentElement.querySelector(selector);
                    if (!currentElement) {
                        console.error(`Elemento com o seletor \"${selector}\" não encontrado.`);
                        return null;
                    }
                    if (currentElement.shadowRoot) {
                        currentElement = currentElement.shadowRoot;
                    }
                }
                return currentElement;
            }

            // Selectors corrigidos para o caminho até o input
            const selectorsForInput = [
                'chassi-root',
                'chassi-page-layout',
                'mat-side-nav-container > mat-side-nav:nth-of-type(2)',
                'chassi-switch-accounts-menu',
                'chassi-card-mf-wrapper',
                'mf-lista-contas',
                'app-main',
                'app-list-accounts',
                'section ul.ids-list'
            ];

            // CNPJ a ser digitado
            const cnpj = "12345678000100"; // Substituído por dados fictícios

            // Digita o CNPJ no campo de entrada
            const inputElement = getElementsInsideNestedShadowRoots(selectorsForInput);
            if (inputElement) {
                inputElement.value = cnpj;
                inputElement.dispatchEvent(new Event("input", { bubbles: true }));
                console.log("CNPJ digitado com sucesso no campo de entrada.");
            } else {
                console.error("Não foi possível encontrar o campo de entrada para o CNPJ.");
            }
            """
            driver.execute_script(script)

            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='printPDF']"))
            ).click()

            time.sleep(2)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
            time.sleep(2)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"Erro durante o loop de comprovantes: {e}")
    finally:
        # Fechar o navegador
        time.sleep(5)
        driver.quit()

def date_calc():
    # Função para calcular datas
    today = datetime.today()
    dia_atual = today.strftime('%d')
    mes_atual = today.strftime('%m')
    ano_atual = today.strftime('%Y')
    day_week = today.weekday()

    if day_week == 0:  # Segunda-feira
        data_anterior = today - timedelta(days=3)
    else:
        data_anterior = today - timedelta(days=1)

    dia_anterior = data_anterior.strftime('%d')
    mes_anterior = data_anterior.strftime('%m')
    ano_anterior = data_anterior.strftime('%Y')

    return {
        "dia_atual": dia_atual,
        "mes_atual": mes_atual,
        "ano_atual": ano_atual,
        "dia_anterior": dia_anterior,
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior
    }

# Executar todas as funções em sequência
dates = date_calc()
login_itau()
acesso_contas_pagar()
loop_comprovantes()
