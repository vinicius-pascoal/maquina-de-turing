from core.turing_machine import TuringMachine
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def handler(event, context):
    """Executa N passos ou até parar"""
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})

        machine_data = body.get('machine')
        steps = body.get('steps', 1)
        max_steps = body.get('max_steps', 1000)

        if not machine_data:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Dados da máquina ausentes'
                })
            }

        tm = TuringMachine.from_dict(machine_data)

        if steps == -1:  # Rodar até parar
            steps_executed = tm.run(max_steps)
        else:  # Rodar N passos
            steps_executed = 0
            for _ in range(min(steps, max_steps)):
                if tm.halted:
                    break
                tm.step()
                steps_executed += 1

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'machine': tm.to_dict(),
                'steps_executed': steps_executed
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Erro no servidor: {str(e)}'
            })
        }
