
/* vai me ajudar ao escrver relatorio XD */
export function salvarResultado(
    arquitetura: string, tamanhoMB: number, cliente: number, 
    duracaoMs: number
){
    /* salvando arquivo com a lib std (fs)-> file system do node (rust tbm tem) */
    require("fs").appendFileSync("resultados.csv", 
        `${arquitetura},${tamanhoMB},${cliente},${duracaoMs}\n`
    )

}