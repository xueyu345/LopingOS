class GPU:
    def __init__(self, memory_size=16384, num_sms=4, num_cores_per_sm=8):
        # 显存
        self.memory = [0] * memory_size
        self.memory_size = memory_size
        # 流处理器阵列
        self.sms = []
        self.num_sms = num_sms
        self.num_cores_per_sm = num_cores_per_sm
        # 创建流处理器
        for i in range(num_sms):
            self.sms.append(StreamingMultiprocessor(i, num_cores_per_sm))
        # 命令队列
        self.command_queue = []
        # 运行状态
        self.running = False
        # 帧缓冲区
        self.frame_buffer = []
        self.screen_width = 800
        self.screen_height = 600
        # 纹理内存
        self.texture_memory = {}
    
    def initialize(self, width, height):
        """初始化GPU"""
        self.screen_width = width
        self.screen_height = height
        self.frame_buffer = [[0] * width for _ in range(height)]
        self.running = True
        print(f"GPU initialized with {self.num_sms} SMs, {self.num_cores_per_sm} cores per SM")
        print(f"Frame buffer: {width}x{height}")
    
    def allocate_memory(self, size):
        """分配显存"""
        # 简单的内存分配实现
        for i in range(self.memory_size - size + 1):
            # 检查内存区域是否全为0
            free = True
            for j in range(size):
                if self.memory[i + j] != 0:
                    free = False
                    break
            if free:
                return i
        return -1  # 内存不足
    
    def free_memory(self, address, size):
        """释放显存"""
        for i in range(address, address + size):
            self.memory[i] = 0
    
    def load_program(self, program, address):
        """加载着色器程序到显存"""
        for i, instruction in enumerate(program):
            if address + i < self.memory_size:
                self.memory[address + i] = instruction
    
    def enqueue_command(self, command):
        """将命令加入队列"""
        self.command_queue.append(command)
    
    def process_commands(self):
        """处理命令队列"""
        processed = 0
        while self.command_queue and self.running:
            command = self.command_queue.pop(0)
            self._execute_command(command)
            processed += 1
        return processed
    
    def _execute_command(self, command):
        """执行单个命令"""
        cmd_type = command[0]
        if cmd_type == 'CLEAR':
            self._clear_framebuffer(command[1])
        elif cmd_type == 'DRAW_TRIANGLE':
            self._draw_triangle(*command[1:])
        elif cmd_type == 'DRAW_LINE':
            self._draw_line(*command[1:])
        elif cmd_type == 'DRAW_RECT':
            self._draw_rect(*command[1:])
        elif cmd_type == 'RUN_COMPUTE':
            self._run_compute(*command[1:])
        elif cmd_type == 'HALT':
            self.running = False
        else:
            print(f"Unknown command: {cmd_type}")
    
    def _clear_framebuffer(self, color):
        """清除帧缓冲区"""
        for y in range(self.screen_height):
            for x in range(self.screen_width):
                self.frame_buffer[y][x] = color
        print(f"Framebuffer cleared with color {color}")
    
    def _draw_pixel(self, x, y, color):
        """绘制单个像素"""
        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
            self.frame_buffer[y][x] = color
    
    def _draw_line(self, x1, y1, x2, y2, color):
        """绘制线段（Bresenham算法）"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        while True:
            self._draw_pixel(x, y, color)
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    def _draw_triangle(self, v1, v2, v3, color):
        """绘制三角形"""
        # 简单实现：绘制三条边
        self._draw_line(v1[0], v1[1], v2[0], v2[1], color)
        self._draw_line(v2[0], v2[1], v3[0], v3[1], color)
        self._draw_line(v3[0], v3[1], v1[0], v1[1], color)
    
    def _draw_rect(self, x, y, width, height, color):
        """绘制矩形"""
        self._draw_line(x, y, x + width, y, color)
        self._draw_line(x + width, y, x + width, y + height, color)
        self._draw_line(x + width, y + height, x, y + height, color)
        self._draw_line(x, y + height, x, y, color)
    
    def _run_compute(self, kernel, data_address, result_address, size):
        """运行计算内核"""
        # 并行处理数据
        batch_size = (size + self.num_sms - 1) // self.num_sms
        
        for sm_id, sm in enumerate(self.sms):
            start = sm_id * batch_size
            end = min(start + batch_size, size)
            if start < size:
                # 模拟SM执行
                results = sm.execute_kernel(kernel, self.memory, data_address + start, end - start)
                # 将结果写回显存
                for i, result in enumerate(results):
                    if result_address + start + i < self.memory_size:
                        self.memory[result_address + start + i] = result
        
        print(f"Compute kernel executed on {size} elements")
    
    def get_framebuffer(self):
        """获取帧缓冲区"""
        return self.frame_buffer
    
    def dump_memory(self, start, end):
        """打印显存内容"""
        print(f"=== GPU Memory [{start}-{end}] ===")
        for i in range(start, min(end + 1, self.memory_size)):
            print(f"{i:04X}: {self.memory[i]}")
        print("================")
    
    def shutdown(self):
        """关闭GPU"""
        self.running = False
        print("GPU shutdown")

class StreamingMultiprocessor:
    def __init__(self, id, num_cores):
        self.id = id
        self.num_cores = num_cores
        self.cores = [Core(i) for i in range(num_cores)]
        self.shared_memory = [0] * 1024  # 1KB共享内存
    
    def execute_kernel(self, kernel, global_memory, data_address, size):
        """执行计算内核"""
        results = []
        # 每个核心处理一部分数据
        batch_size = (size + self.num_cores - 1) // self.num_cores
        
        for core_id, core in enumerate(self.cores):
            start = core_id * batch_size
            end = min(start + batch_size, size)
            if start < size:
                # 核心执行
                core_results = core.execute(kernel, global_memory, data_address + start, end - start)
                results.extend(core_results)
        
        return results
    
    def __str__(self):
        return f"SM_{self.id}({self.num_cores} cores)"

class Core:
    def __init__(self, id):
        self.id = id
        self.registers = [0] * 32  # 32个寄存器
    
    def execute(self, kernel, global_memory, data_address, size):
        """执行指令"""
        results = []
        
        for i in range(size):
            # 加载数据
            data = global_memory[data_address + i]
            # 执行内核函数
            result = kernel(data)
            results.append(result)
        
        return results

# 示例内核函数
def add_one_kernel(x):
    """简单的加1内核"""
    return x + 1

def square_kernel(x):
    """平方内核"""
    return x * x

# 测试代码
if __name__ == "__main__":
    # 创建GPU实例
    gpu = GPU(memory_size=16384, num_sms=4, num_cores_per_sm=8)
    
    # 初始化GPU
    gpu.initialize(800, 600)
    
    # 测试内存分配
    addr = gpu.allocate_memory(10)
    print(f"Allocated memory at address: {addr}")
    
    # 加载测试数据
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i, data in enumerate(test_data):
        gpu.memory[addr + i] = data
    
    # 分配结果内存
    result_addr = gpu.allocate_memory(10)
    print(f"Allocated result memory at address: {result_addr}")
    
    # 运行计算内核
    gpu._run_compute(square_kernel, addr, result_addr, 10)
    
    # 显示结果
    print("=== Computation Results ===")
    for i in range(10):
        print(f"Input: {test_data[i]}, Output: {gpu.memory[result_addr + i]}")
    print("========================")
    
    # 测试图形渲染
    print("\n=== Graphics Tests ===")
    
    # 清除帧缓冲区
    gpu.enqueue_command(('CLEAR', 0x000000))  # 黑色
    
    # 绘制三角形
    gpu.enqueue_command(('DRAW_TRIANGLE', (100, 100), (200, 50), (150, 200), 0xFF0000))  # 红色
    
    # 绘制线段
    gpu.enqueue_command(('DRAW_LINE', 50, 50, 250, 250, 0x00FF00))  # 绿色
    
    # 绘制矩形
    gpu.enqueue_command(('DRAW_RECT', 300, 100, 150, 100, 0x0000FF))  # 蓝色
    
    # 处理命令
    processed = gpu.process_commands()
    print(f"Processed {processed} commands")
    
    # 检查帧缓冲区
    print(f"Frame buffer size: {len(gpu.frame_buffer)}x{len(gpu.frame_buffer[0])}")
    print("Sample pixel at (100, 100):", gpu.frame_buffer[100][100])
    
    # 释放内存
    gpu.free_memory(addr, 10)
    gpu.free_memory(result_addr, 10)
    
    # 关闭GPU
    gpu.shutdown()