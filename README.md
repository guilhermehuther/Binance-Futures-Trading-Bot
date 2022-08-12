# Binance Futures Trading Bot <img src="https://user-images.githubusercontent.com/86479393/184355244-481519ab-fdca-45e6-bc5f-1f23f5599046.png" width="40" height="40"><img src="https://user-images.githubusercontent.com/86479393/183930853-bd8bc5de-c1b4-4a8f-a302-23880b31ad7c.png" width="40" height="40"> 

## Pré-requisitos
  1. requirements.txt
  2. Binance api key/secret (https://www.youtube.com/watch?v=_4IgARHj6TY&ab_channel=TradingcomDados)
  3. Estratégia 
  4. Python == 3.10.4
  
## Síntese
  `O programa consiste em`: Operar na Binance futures, a partir de indicadores/estratégias, com/sem alavancagem.

## Instruções

```ruby
# Função que conterá a estratégia a partir dos indicadores desejados. Mandatório "Sell" para short ou "Buy" para long como retorno.
12 def strategy(df):
```
```ruby
# Interval == Tempo gráfico das candles retornadas / start_str == Gráfico histórico do símbolo
34 df = pd.DataFrame(client.futures_historical_klines(symbol = symbol, interval = "15m", limit = 1000, start_str = "5 days ago UTC"))
```
```ruby
# Colocar indicadores que serão alimentados para a função "strategy", também, mudar os nomes dos indicadores na função.
42  ### Indicadores
```
```ruby
# Recomendo o uso de uma quantidade fixa como valor de entrada de cada operação.
58 quantity = str(0.01) 
```
```ruby
# True == utilizar Take profit e Stop loss como fim das operações.
60 tpsl = False
61 tp = 5
61 sl = 3

# True == utilizar as indicações da estratégia como fim das operações.
64 strategycalls = True
```


## Recomendações

- NÂO ME RESPONSABILIZO POR QUAISQUER PERDAS PROVENIENTES DO USO DESSE BOT, O COMPARTILHO APENAS PARA FINS EDUCATIVOS.
- A estratégia existente no bot é meramente um exemplo de como o código deverá ser estruturado.
- Trocar a alavancagem manualmente na Binance futures.
- Estudo prévio sobre o funcionamento da plataforma.
- Analisar qual moeda e tempo gráfico funciona de forma mais eficiente na sua estratégia.
