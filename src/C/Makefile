

TARGET ?= exe
SRC_DIRS ?= ./src
LIBTARGET ?= libcalculator.so

SRCS := $(shell find $(SRC_DIRS) -name *.cpp -or -name *.c -or -name *.s)
OBJS := $(addsuffix .o,$(basename $(SRCS)))
DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIRS) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

CPPFLAGS ?= $(INC_FLAGS) -MMD -MP -Wall -fPIC
LDFLAGS :=

#CPPFLAGS ?= $(INC_FLAGS) -MMD -MP -g -O0
#LDFLAGS := -g -O0

.PHONY: lib
lib: $(LIBTARGET)

$(TARGET): clean $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) -o $@ $(LOADLIBES) $(LDLIBS)

$(LIBTARGET): clean $(OBJS)
	$(CC) -shared $(OBJS) -o $@ $(LOADLIBES) $(LDLIBS)

.PHONY: clean
clean:
	$(RM) $(TARGET) $(OBJS) $(DEPS) $(LIBTARGET)

.PHONY: run
run: clean $(TARGET)
	./$(TARGET)

.PHONY: python
python: clean lib
	python3 simulation.py

.PHONY: gdb
gdb: clean $(TARGET)
	gdb ./$(TARGET)

-include $(DEPS)


