/* Gerando arquivos falsos para fazer nossos testes */

export function gerarArquivo(tamanhoMB: number): Buffer {

    /* cripto random bytes stdlib node que gera bytes */
    return require("crypto").randomBytes(tamanhoMB * 1024 * 1024)

    
}