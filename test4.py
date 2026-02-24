class Student:
    def __init__(self, name, score, class_name=None):
        self.name = name
        self.score = score
        self.class_name = class_name  # 新增班级信息
    
    def __str__(self):
        return f"姓名: {self.name}, 分数: {self.score}, 班级: {self.class_name}"
    
    def sort_by_score(self, students, reverse=False):
        """
        按分数排序并逐行打印学生信息
        
        参数:
            students: 学生列表
            reverse: 是否降序排序，默认为False(升序)
        """
        # 按分数排序
        sorted_students = sorted(students, key=lambda x: x.score, reverse=reverse)
        
        # 逐行打印学生信息
        for student in sorted_students:
            print(student)

# 示例使用
if __name__ == "__main__":
    # 创建学生列表
    students = [
        Student("张三", 85, "一班"),
        Student("李四", 92, "二班"),
        Student("王五", 78, "一班"),
        Student("赵六", 88, "三班")
    ]
    
    # 创建一个学生对象用于调用方法
    s = Student("", 0)
    
    # 按分数升序排序并打印
    print("按分数升序排序:")
    s.sort_by_score(students)
    
    # 按分数降序排序并打印
    print("\n按分数降序排序:")
    s.sort_by_score(students, reverse=True)
