
TARGET	=	whistlecalc
DEPS	=	main.py \
			main_frame.py \
			calculate.py \
			line_widgit.py \
			hole_widgit.py \
			data_store.py \
			upper_frame.py \
			lower_frame.py \
			utiltiy.py \
			dialogs.py

all: $(TARGET)

$(TARGET): $(DEPS)
	pyinstaller -F -n whistlecalc main.py

clean:
	rm -rf *.spec dist build __pycache__ *.wis