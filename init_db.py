import os
import sys
from database import init_db, import_questions_from_txt, create_user

# Create sample question files
def create_sample_data():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/questions', exist_ok=True)
    
    # Sample data for operating systems
    os_questions = """什么是操作系统？
A. 一种应用程序
B. 计算机硬件与用户之间的接口
C. 一种编程语言
D. 一种网络协议
答案: B
解析: 操作系统是计算机硬件与用户之间的接口，管理计算机硬件资源，为用户程序提供服务。

进程和线程的主要区别是什么？
A. 进程是资源分配的基本单位，线程是CPU调度的基本单位
B. 进程比线程更轻量级
C. 线程无法共享内存空间
D. 进程只能在单核CPU上运行
答案: A
解析: 进程是资源分配的基本单位，拥有独立的地址空间；线程是CPU调度的基本单位，共享所属进程的地址空间。

死锁的必要条件包括哪些？
A. 互斥、持有并等待、非抢占、循环等待
B. 互斥、共享资源、优先调度
C. 并发、资源分配、进程通信
D. 进程同步、内存管理、处理器调度
答案: A
解析: 死锁产生的四个必要条件是：互斥、持有并等待、非抢占和循环等待。

虚拟内存的主要作用是什么？
A. 提高CPU运行速度
B. 扩大可用内存空间
C. 提高磁盘I/O速度
D. 增强系统安全性
答案: B
解析: 虚拟内存使用磁盘空间作为内存的扩展，使得程序可以使用比实际物理内存更大的地址空间。

分页和分段的主要区别是什么？
A. 分页是物理单位，分段是逻辑单位
B. 分页更容易产生外部碎片
C. 分段不支持虚拟内存
D. 分页只用于大型操作系统
答案: A
解析: 分页是将内存分成固定大小的块，是一种物理单位；分段是根据程序的逻辑结构划分，是一种逻辑单位。
"""

    # Sample data for data structures
    ds_questions = """什么是栈？
A. 先进先出(FIFO)的数据结构
B. 后进先出(LIFO)的数据结构
C. 随机访问的数据结构
D. 无序的数据集合
答案: B
解析: 栈是一种后进先出(LIFO)的数据结构，只能在一端(栈顶)进行插入和删除操作。

二叉搜索树的特点是什么？
A. 每个节点有且仅有两个子节点
B. 左子树所有节点的值都小于根节点，右子树所有节点的值都大于根节点
C. 所有叶节点都在同一层
D. 根节点一定是最大值
答案: B
解析: 二叉搜索树满足对任意节点，其左子树所有节点值都小于该节点，右子树所有节点值都大于该节点。

快速排序的平均时间复杂度是多少？
A. O(n)
B. O(n log n)
C. O(n²)
D. O(log n)
答案: B
解析: 快速排序的平均时间复杂度是O(n log n)，最坏情况下为O(n²)。

哈希表的主要优势是什么？
A. 节省内存空间
B. 提供有序的数据存储
C. 支持快速的查找操作
D. 便于数据压缩
答案: C
解析: 哈希表通过哈希函数将键映射到存储位置，从而支持O(1)时间复杂度的快速查找操作。

图的广度优先搜索(BFS)使用什么数据结构来实现？
A. 栈
B. 队列
C. 数组
D. 集合
答案: B
解析: 图的广度优先搜索(BFS)通常使用队列来实现，以便按层次遍历图中的节点。
"""

    # Sample data for networks
    network_questions = """OSI模型有几层？
A. 5层
B. 6层
C. 7层
D. 8层
答案: C
解析: OSI模型由国际标准化组织(ISO)提出，分为物理层、数据链路层、网络层、传输层、会话层、表示层和应用层共7层。

TCP和UDP的主要区别是什么？
A. TCP是面向连接的，UDP是无连接的
B. TCP比UDP传输速度更快
C. UDP提供可靠传输，TCP不提供
D. TCP只用于局域网通信
答案: A
解析: TCP是面向连接的协议，提供可靠的数据传输；UDP是无连接的协议，不保证数据传输的可靠性但速度更快。

IP地址的主要作用是什么？
A. 标识网络中的物理设备
B. 加密网络数据
C. 标识网络中的应用程序
D. 提高网络传输速度
答案: A
解析: IP地址用于在网络中唯一标识一个设备（主机或路由器），使网络能够正确地转发数据包。

什么是HTTP状态码302？
A. 请求成功
B. 临时重定向
C. 服务器错误
D. 未找到资源
答案: B
解析: HTTP状态码302表示临时重定向，表明请求的资源已临时移动到Location头部指定的URL。

DNS服务的主要功能是什么？
A. 分配IP地址
B. 域名解析
C. 网络安全防护
D. 数据压缩传输
答案: B
解析: DNS(域名系统)的主要功能是将域名解析为IP地址，使用户可以通过易记的域名访问网络资源。
"""

    # Write sample data to files
    with open('data/questions/操作系统.txt', 'w', encoding='utf-8') as f:
        f.write(os_questions)
    
    with open('data/questions/数据结构.txt', 'w', encoding='utf-8') as f:
        f.write(ds_questions)
    
    with open('data/questions/计算机网络.txt', 'w', encoding='utf-8') as f:
        f.write(network_questions)
    
    print("创建示例题目数据完成！")

def main():
    print("初始化数据库...")
    init_db()
    
    print("创建示例数据...")
    create_sample_data()
    
    print("导入题目到数据库...")
    questions_dir = 'data/questions'
    if os.path.exists(questions_dir):
        for filename in os.listdir(questions_dir):
            if filename.endswith('.txt'):
                category = os.path.splitext(filename)[0]
                file_path = os.path.join(questions_dir, filename)
                print(f"导入 {category} 类别的题目...")
                import_questions_from_txt(file_path, category)
    
    # Create test user
    print("创建测试用户...")
    create_user('test', 'test123', 'test@example.com')
    
    print("数据库初始化完成！")

if __name__ == "__main__":
    main() 