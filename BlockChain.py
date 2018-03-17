from Block import *
class BlockChain:
    def __init__(self):
        self.chain = list[Block]




    def is_valid(self):
        for i in range(1, len(self.chain)):
            last_block = self.chain(i-1)
            current_block = self.chain(i)
            if current_block.hash != current_block.compute_hash:
                return False
            if last_block.hash != current_block.last_hash:
                return False

        return True





