import requests
import logging

api = 'https://chain.api.btc.com/v3/tx/'
transactions = [
    'ca68e6a6a31fa5cb8d6f1df24f8d012a7e48f39952ed8d788a3cadf63944674b',
    'cf243808d7ed04d541e1da265466b25859ccc8f88ba109d0e54869a4f838e942',
    '31c26e86d9ed0230516d80ad1da978b5a58c0e33c2f85fa7d446be2336a24351',
    '17e4e4e0944529498ee8ef0f87f38619f068a79ff909d87bea06220c4c363899',
    '2fc45d6a2418b3bff2f5fa08c954af5a875798f88e736750e89c8cdd2ca31e46',
    'c15af71d15a358647faae61750d21914e792b7ed1fb3e6210881e6991c09b7ee',
    'eb73ae2969de44d9089e65d9c662ecd7cdc39e8501b6c97060f9107f9ef0d7e2',
    '427525e89f9b535968eca8f40a845698eeb130bae0824d2cf062d44268c383cc',
    '0ce3c22b5c8fa81f58c67cac71d0da4f1b1a245a0f639bc62017cc70c9feb77a',
    '2c7d606ac437104897be89c7773e9830ab330c7eda97760cae8428a0810f917a',
    '49f3facb47495ff627784168d1a5112c976dca8c6086009a271733906aa3dfb5',
    '47432d0a45044eb1f99060884a600b8508777e97de3bb8faee88fdf4724eae6c',
    '3b651c8d80679bfd427a6ff30dbb0f19e5abb8c130df502a0680b9d95b0b3580',
    'f52e039732652a15b63c4966711953575dbbfee343745e4d0b55d899e5ea9cb0',
    '0368a29bd199e359c6b80a1c5ee75cd75f2725ab94ce8d0904f3537d35e07452',
    '86649e447d12f3e5b3ff4563ca0fd4e0da9f5350394698c8e6bbd3c0d86bf5e6',
    '4322f9b51ec4c99921abe7654d57a0877a99c8228466508d5d5666844a19af23',
    'a77a3194c67c3355ee4ae84d08e9145744c4c94c14ca0ce747c49daef1288d1b'
]
logging.basicConfig(level=logging.WARNING, format='')
mylogger = logging.getLogger()


def get_input_spent(tx, depth, prev):
    response = requests.get(api + tx).json()['data']
    if response['confirmations'] > 0:
        # mylogger.warning('\tConfirmed: ' + tx + ' depth: ' + str(depth))
        mylogger.warning('\tDouble Spended, By: ' + response['outputs'][prev]['spent_by_tx'] +
                         ' Position: ' + str(response['outputs'][prev]['spent_by_tx_position']))
        return depth
    for input in response['inputs']:
        if input['sequence'] < 0xffffffff - 1:
            # print 'RBF'
            mylogger.warning('\tRBF transaction: ' + tx)
        return get_input_spent(input['prev_tx_hash'], depth + 1, input['prev_position'])


for tran in transactions:
    mylogger.warning('Transaction: ' + tran)
    depth = get_input_spent(tran, 0, -1)
    # print depth
    if depth != 2:
        print 'Wrong : ' + tran


