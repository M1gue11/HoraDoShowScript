all:
	@python main.py
	@gcc -o exec programa_hora_do_show.c
	@./exec
	# @rm exec
