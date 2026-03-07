class CPU:
    def __init__(self, memory_size=4096):
        # 通用寄存器
        self.registers = {
            'R0': 0,  # 零寄存器
            'R1': 0,
            'R2': 0,
            'R3': 0,
            'R4': 0,
            'R5': 0,
            'R6': 0,
            'R7': 0,
            'PC': 0,  # 程序计数器
            'SP': memory_size - 1,  # 栈指针
            'FLAGS': 0  # 标志寄存器
        }
        # 内存
        self.memory = [0] * memory_size
        # 指令集
        self.instructions = {
            'ADD': self._add,
            'SUB': self._sub,
            'MOV': self._mov,
            'LOAD': self._load,
            'STORE': self._store,
            'JMP': self._jmp,
            'JZ': self._jz,
            'JNZ': self._jnz,
            'PUSH': self._push,
            'POP': self._pop,
            'HALT': self._halt
        }
        # 运行状态
        self.running = False
    
    def _add(self, dst, src):
        """加法指令: dst = dst + src"""
        if isinstance(src, str):
            src_value = self.registers[src]
        else:
            src_value = src
        result = self.registers[dst] + src_value
        self.registers[dst] = result
        self._update_flags(result)
    
    def _sub(self, dst, src):
        """减法指令: dst = dst - src"""
        if isinstance(src, str):
            src_value = self.registers[src]
        else:
            src_value = src
        result = self.registers[dst] - src_value
        self.registers[dst] = result
        self._update_flags(result)
    
    def _mov(self, dst, src):
        """移动指令: dst = src"""
        if isinstance(src, str):
            self.registers[dst] = self.registers[src]
        else:  # 立即数
            self.registers[dst] = src
    
    def _load(self, dst, addr):
        """加载指令: dst = memory[addr]"""
        if isinstance(addr, str):
            addr = self.registers[addr]
        self.registers[dst] = self.memory[addr]
    
    def _store(self, src, addr):
        """存储指令: memory[addr] = src"""
        if isinstance(addr, str):
            addr = self.registers[addr]
        self.memory[addr] = self.registers[src]
    
    def _jmp(self, addr):
        """无条件跳转指令: PC = addr"""
        if isinstance(addr, str):
            self.registers['PC'] = self.registers[addr]
        else:
            self.registers['PC'] = addr
    
    def _jz(self, addr):
        """零标志跳转指令: 如果ZF=1，PC=addr"""
        if (self.registers['FLAGS'] & 1) == 1:
            self._jmp(addr)
        else:
            self.registers['PC'] += 1
    
    def _jnz(self, addr):
        """非零标志跳转指令: 如果ZF=0，PC=addr"""
        if (self.registers['FLAGS'] & 1) == 0:
            self._jmp(addr)
        else:
            self.registers['PC'] += 1
    
    def _push(self, src):
        """压栈指令: 将src的值压入栈"""
        if isinstance(src, str):
            value = self.registers[src]
        else:
            value = src
        self.memory[self.registers['SP']] = value
        self.registers['SP'] -= 1
    
    def _pop(self, dst):
        """出栈指令: 从栈中弹出值到dst"""
        self.registers['SP'] += 1
        self.registers[dst] = self.memory[self.registers['SP']]
    
    def _halt(self):
        """停机指令"""
        self.running = False
    
    def _update_flags(self, result):
        """更新标志寄存器"""
        # 零标志 (ZF)
        zf = 1 if result == 0 else 0
        # 符号标志 (SF)
        sf = 1 if result < 0 else 0
        # 溢出标志 (OF) - 简化实现
        of = 0
        self.registers['FLAGS'] = (of << 2) | (sf << 1) | zf
    
    def load_program(self, program, start_addr=0):
        """加载程序到内存"""
        for i, instruction in enumerate(program):
            self.memory[start_addr + i] = instruction
        self.registers['PC'] = start_addr
    
    def step(self):
        """单步执行"""
        if not self.running:
            return False
        
        # 取指
        pc = self.registers['PC']
        instruction = self.memory[pc]
        
        # 解码执行
        if isinstance(instruction, tuple):
            op = instruction[0]
            args = instruction[1:]
            if op in self.instructions:
                self.instructions[op](*args)
            else:
                print(f"Unknown instruction: {op}")
                self.running = False
        else:
            print(f"Invalid instruction at {pc}: {instruction}")
            self.running = False
        
        # 更新程序计数器
        if self.running and op not in ['JMP', 'JZ', 'JNZ']:
            self.registers['PC'] += 1
        
        return self.running
    
    def run(self, steps=None):
        """运行程序"""
        self.running = True
        step_count = 0
        
        while self.running and (steps is None or step_count < steps):
            self.step()
            step_count += 1
        
        return step_count
    
    def dump_registers(self):
        """打印寄存器状态"""
        print("=== Registers ===")
        for reg, value in self.registers.items():
            print(f"{reg}: {value:04X}")
        print("================")
    
    def dump_memory(self, start, end):
        """打印内存状态"""
        print(f"=== Memory [{start}-{end}] ===")
        for i in range(start, end + 1):
            print(f"{i:04X}: {self.memory[i]}")
        print("================")

# 示例程序: 计算1+2+3+...+10
example_program = [
    ('MOV', 'R1', 1),      # R1 = 1 (计数器)
    ('MOV', 'R2', 0),      # R2 = 0 (累加器)
    ('MOV', 'R3', 10),     # R3 = 10 (上限)
    ('ADD', 'R2', 'R1'),   # R2 = R2 + R1
    ('ADD', 'R1', 1),      # R1 = R1 + 1
    ('SUB', 'R4', 'R1', 'R3'),  # R4 = R1 - R3
    ('JNZ', 3),            # 如果R4 != 0，跳转到地址3
    ('HALT',)              # 停机
]

# 修正SUB指令参数
example_program[5] = ('MOV', 'R4', 'R1')
example_program.insert(6, ('SUB', 'R4', 'R3'))

# 测试CPU
if __name__ == "__main__":
    cpu = CPU()
    
    # 加载程序
    cpu.load_program(example_program)
    
    # 运行程序
    print("Running example program...")
    steps = cpu.run()
    print(f"Program finished in {steps} steps")
    
    # 打印结果
    cpu.dump_registers()
    print(f"Sum of 1-10: {cpu.registers['R2']}")