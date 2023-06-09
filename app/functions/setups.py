from assets.setups.ff_fd import ff_fd
from assets.setups.inside_bar import inside_bar
from assets.setups.max_min import max_min
from assets.setups.pfr import pfr
from assets.setups.rsi_2 import rsi_2
from assets.setups.setup_123 import setup_123
from assets.setups.setup_9_1 import setup_9_1

frequency = {'Diário': 'd', 'Semanal': 'wk'}

setups_info = {'Fechou Fora, Fechou Dentro': 'ff_fd', 
          'Inside Bar': 'inside_bar', 
          'Máximas e Mínimas': 'max_min', 
          'Preço de Fechamento de Reversão': 'pfr', 
          'RSI-2': 'rsi_2', 
          'Setup 123 de Compra': 'setup_123', 
          'Larry Williams 9.1': 'setup_9_1'}

setups_function = {'ff_fd': ff_fd, 
                   'inside_bar': inside_bar, 
                   'max_min': max_min, 
                   'pfr': pfr, 
                   'rsi_2': rsi_2, 
                   'setup_123': setup_123, 
                   'setup_9_1': setup_9_1}

setups_description = {
    'ff_fd': {'condition': 'Bandas de Bollinger 20 periodos.',
              'entry': 'Rompimento imediato da máxima do primeiro candle que fechou dentro da Banda de Bollinger.',
              'target': 'Banda central da Bollinger, média móvel de 20.',
              'stop': 'Perda da mínima do candle gatilho.'},
    'inside_bar': {'condition': 'Máxima menor que candle anterior e mínima maior que candle anterior',
                   'entry': 'Rompimento da máxima do inside bar (cancelada se houver perda da mínima do inside bar).',
                   'target': '2x amplitude do inside bar.',
                   'stop': 'Perda da mínima do candle (inside bar) gatilho.'},
    'max_min': {'condition': 'Não há.',
                'entry': 'Mínima dos 2 últimos candles',
                'target': 'Não há.',
                'stop': 'Máxima dos 2 últimos candles.'},
    'pfr': {'condition': 'Candle PFR (mínima menor que as 2 últimas e fechamento maior que candle anterior).',
            'entry': 'Rompimento da máxima do candle PFR (cancelada se houver perda da mínima do candle PFR).',
            'target': '2x amplitude do candle PFR.',
            'stop': 'Perda da mínima do candle (PFR) gatilho.'},
    'rsi_2': {'condition': 'RSI 2 períodos.',
              'entry': 'Fechamento do candle com RSI menor que 25.',
              'target': 'Máxima dos 2 últimos candles.',
              'stop': 'Após 7 candles.'},
    'setup_123': {'condition': '123 (candle 1 com mínima maior que candle 2 cuja mínima é menor que candle 3).',
                  'entry': 'Rompimento da máxima do terceiro candle (cancelada se houver perda da menor mínima do 123).',
                  'target': '2x amplitude do 123 (da maior máxima até menor mínima).',
                  'stop': 'Perda da menor mínima do 123.'},
    'setup_9_1': {'condition': 'Média móvel exponencial 9 períodos.',
                  'entry': 'Rompimento da máxima do candle que virar a mme9 para cima.',
                  'target': 'Perda da mínima do candle que virar a mme9 para baixo (cancelado se mme9 virar para cima).',
                  'stop': 'Perda da mínima do candle gatilho.'}
}