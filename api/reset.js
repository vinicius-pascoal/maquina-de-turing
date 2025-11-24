import { parseSpec } from '../core/turing_machine.js';

export default function handler(req, res) {
  try {
    const { spec, input = '' } = req.body;

    if (!spec) {
      return res.status(400).json({
        success: false,
        error: 'Especificação vazia'
      });
    }

    const { tm, error } = parseSpec(spec);

    if (error) {
      return res.status(400).json({
        success: false,
        error
      });
    }

    tm.reset(input);

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
