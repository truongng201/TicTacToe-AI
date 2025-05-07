.PHONY: minimiax alphabeta mcts qplayer

minimax:
	echo "minimax vs random"; \
	python3 main.py --player1 minimax --player2 random --mode silent --num_games 100
	echo "minimax vs minimax"; \
	python3 main.py --player1 minimax --player2 minimax --mode silent --num_games 100
	echo "minimax vs human"; \
	python3 main.py --player1 minimax --player2 human --num_games 10

alphabeta:
	echo "alphabeta vs minimax"; \
	python3 main.py --player1 alphabeta --player2 minimax --mode silent --num_games 20
	
mcts:
	echo "mcts vs random"; \
	python3 main.py --player1 mcts --player2 random --mode silent --num_games 100
	echo "mcts vs alphabeta"; \
	python3 main.py --player1 mcts --player2 alphabeta --mode silent --num_games 100

qplayer:
	echo "qplayer vs random"; \
	python3 main.py --player1 qplayer --player2 random --mode silent --num_games 100
	echo "qplayer vs minimax"; \
	python3 main.py --player1 qplayer --player2 minimax --mode silent --num_games 100
	echo "qplayer vs mcts"; \
	python3 main.py --player1 qplayer --player2 mcts --mode silent --num_games 100
	echo "qplayer vs alphabeta"; \
	python3 main.py --player1 qplayer --player2 alphabeta --mode silent --num_games 100
	echo "qplayer vs qplayer"; \
	python3 main.py --player1 qplayer --player2 qplayer --mode silent --num_games 100