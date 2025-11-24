#!/usr/bin/env python3
"""
Script de teste local para as APIs da Máquina de Turing
Execute este script para testar todas as APIs localmente
"""

from core.examples import EXAMPLES
from core.turing_machine import parse_spec, TuringMachine
import json
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_validate():
    """Testa a validação de especificação"""
    print("\n=== Testando VALIDATE ===")

    spec = """
states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,1,R
q0,1 -> q0,1,R
q0,_ -> qaccept,_,N
q1,0 -> q0,0,R
q1,1 -> q1,1,R
q1,_ -> qreject,_,N
"""

    tm, error = parse_spec(spec)

    if error:
        print(f"❌ Erro: {error}")
        return False
    else:
        print(f"✅ Especificação válida!")
        print(f"   Estados: {len(tm.states)}")
        print(f"   Transições: {len(tm.transitions)}")
        return True


def test_reset():
    """Testa o reset da máquina"""
    print("\n=== Testando RESET ===")

    spec = list(EXAMPLES.values())[0]
    input_string = "0011"

    tm, error = parse_spec(spec)

    if error:
        print(f"❌ Erro no parse: {error}")
        return False

    tm.reset(input_string)

    print(f"✅ Máquina inicializada!")
    print(f"   Estado inicial: {tm.current_state}")
    print(f"   Posição da cabeça: {tm.head}")
    print(f"   Fita: {dict(tm.tape)}")
    return True


def test_step():
    """Testa a execução de um passo"""
    print("\n=== Testando STEP ===")

    spec = list(EXAMPLES.values())[0]
    input_string = "0011"

    tm, error = parse_spec(spec)

    if error:
        print(f"❌ Erro no parse: {error}")
        return False

    tm.reset(input_string)

    print(f"Antes do passo:")
    print(f"   Estado: {tm.current_state}")
    print(f"   Posição: {tm.head}")
    print(f"   Símbolo: {tm.read()}")

    tm.step()

    print(f"\nDepois do passo:")
    print(f"   Estado: {tm.current_state}")
    print(f"   Posição: {tm.head}")
    print(f"   Símbolo: {tm.read()}")
    print(f"   Parada: {tm.halted}")

    print(f"✅ Passo executado com sucesso!")
    return True


def test_run():
    """Testa a execução completa"""
    print("\n=== Testando RUN ===")

    spec = list(EXAMPLES.values())[0]
    input_string = "0011"

    tm, error = parse_spec(spec)

    if error:
        print(f"❌ Erro no parse: {error}")
        return False

    tm.reset(input_string)

    steps = tm.run(max_steps=100)

    print(f"✅ Execução completa!")
    print(f"   Passos executados: {steps}")
    print(f"   Estado final: {tm.current_state}")
    print(f"   Resultado: {tm.result}")
    print(f"   Fita final: {dict(tm.tape)}")
    return True


def test_examples():
    """Testa o carregamento de exemplos"""
    print("\n=== Testando EXAMPLES ===")

    print(f"✅ Exemplos carregados: {len(EXAMPLES)}")
    for name in EXAMPLES.keys():
        print(f"   - {name}")
    return True


def test_serialization():
    """Testa serialização/deserialização"""
    print("\n=== Testando SERIALIZAÇÃO ===")

    spec = list(EXAMPLES.values())[0]
    input_string = "01"

    tm, error = parse_spec(spec)

    if error:
        print(f"❌ Erro no parse: {error}")
        return False

    tm.reset(input_string)
    tm.step()

    # Serializar
    data = tm.to_dict()
    print(f"✅ Serializado: {len(json.dumps(data))} bytes")

    # Deserializar
    tm2 = TuringMachine.from_dict(data)
    print(f"✅ Deserializado com sucesso!")

    # Verificar
    assert tm2.current_state == tm.current_state
    assert tm2.head == tm.head
    assert tm2.halted == tm.halted

    print(f"✅ Dados preservados corretamente!")
    return True


def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Iniciando testes das APIs...\n")
    print("=" * 50)

    tests = [
        ("Validate", test_validate),
        ("Reset", test_reset),
        ("Step", test_step),
        ("Run", test_run),
        ("Examples", test_examples),
        ("Serialization", test_serialization),
    ]

    results = []

    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Erro no teste {name}: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("\n📊 RESUMO DOS TESTES:\n")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\n{'='*50}")
    print(f"Total: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 Todos os testes passaram!")
        return 0
    else:
        print("❌ Alguns testes falharam")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
