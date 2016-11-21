# Simulador de SGBD
Integrantes: Gustavo Kath, Paola Salvador, Pedro Vanzella, Jean

## Instalação
Para a execução do trabalho são requeridos
```
Python 3.5.1
Docker
```
### Instalação do Docker
Vá até o site do Docker e faça o download do client do Docker [Download ] (https://www.docker.com/products/overview#/install_the_platform).

Siga os passos na tela para realizar a instalação


## Execução
No diretório do projeto execute o commando make

```
$ make
```

## Comandos suportados
* Inserção de 1 registro
```
insert(code, description)
```

* Inserção de N registros aleatórios
```
insert(N)
```

* Seleção de registro por código
```
select(code)
```

* Seleção de registros por descrição
```
select(description)
```

* Atualizar descrição de registro
```
update(code, new_description)
```

* Remover registro da tabela
```
delete(code)
```

* Sair do SGBD
```
exit
```

* Limpar datafile
```
wipe
```

* Mostrar dados na BTree
```
btree
```
