import { TuringMachine } from '../core/turing_machine.js';

export default function handler(req, res) {
  try {
    const { machine } = req.body;

    if (!machine) {
      return res.status(400).json({
        success: false,
        error: 'Dados da máquina ausentes'
      });
    }

    const tm = TuringMachine.fromDict(machine);
    tm.step();

    return res.status(200).json({
      success: true,
      machine: tm.toDict()
    });
  } catch (e) {
    return res.status(500).json({
      success: false,
      error: `Erro no servidor: ${e.message}`
    });
  }
}
