class Solution:
    def jump(self, nums: list[int]) -> int:
        n = len(nums)
        # Если массив состоит из одного элемента, мы уже у цели
        if n <= 1:
            return 0
        
        jumps = 0
        current_end = 0
        farthest = 0
        
        # Проходим до предпоследнего элемента, 
        # так как дойдя до конца, делать новый прыжок не нужно
        for i in range(n - 1):
            # Обновляем максимально далёкую точку, куда можем допрыгнуть
            farthest = max(farthest, i + nums[i])
            
            # Если дошли до конца текущего прыжка, совершаем следующий прыжок
            if i == current_end:
                jumps += 1
                current_end = farthest
                
                # Ранний выход: если уже можем достать до последнего индекса
                if current_end >= n - 1:
                    break
                    
        return jumps