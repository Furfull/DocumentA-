package main

import (
    "fmt"
)

func main() {
    fmt.Println("Calculadora Simples")
    fmt.Println("Escolha a operação:")
    fmt.Println("1. Adição")
    fmt.Println("2. Subtração")
    fmt.Println("3. Multiplicação")
    fmt.Println("4. Divisão")

    var escolha int
    fmt.Print("Digite o número da operação desejada: ")
    fmt.Scan(&escolha)

    if escolha >= 1 && escolha <= 4 {
        var num1, num2 float64
        fmt.Print("Digite o primeiro número: ")
        fmt.Scan(&num1)
        fmt.Print("Digite o segundo número: ")
        fmt.Scan(&num2)

        switch escolha {
        case 1:
            fmt.Printf("Resultado: %.2f + %.2f = %.2f\n", num1, num2, num1+num2)
        case 2:
            fmt.Printf("Resultado: %.2f - %.2f = %.2f\n", num1, num2, num1-num2)
        case 3:
            fmt.Printf("Resultado: %.2f * %.2f = %.2f\n", num1, num2, num1*num2)
        case 4:
            if num2 != 0 {
                fmt.Printf("Resultado: %.2f / %.2f = %.2f\n", num1, num2, num1/num2)
            } else {
                fmt.Println("Erro: Divisão por zero não é permitida.")
            }
        }
    } else {
        fmt.Println("Opção inválida. Tente novamente.")
    }
}
