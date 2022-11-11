import sys
import pygame
from pygame.locals import *

BLOCK_EDGE_LENGTH = 30
GROUND_GRID_SIZE = 10, 20
GROUND_SIZE = BLOCK_EDGE_LENGTH * GROUND_GRID_SIZE[0] + GROUND_GRID_SIZE[0] - 1,\
		BLOCK_EDGE_LENGTH * GROUND_GRID_SIZE[1] + GROUND_GRID_SIZE[1] - 1
FPS = 60

g_oDisPlay = None
g_oTetris = None

x = y = 0 # 绕着点O(x,y)旋转
MR_clickwise = [
	[0, 1, x - y],
	[-1, 0, x + y],
	[0, 0, 1],
]
MR_anticlickwise = [
	[0, -1, x + y],
	[1, 0, y - x],
	[0, 0, 1],
]


def Main():
	Init()
	Loop()


def Init():
	global g_oDisPlay
	pygame.init()
	g_oDisPlay = pygame.display.set_mode(size=GROUND_SIZE)
	pygame.display.set_caption("tetris")


def Loop():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		GameLoop()
		pygame.display.update()
		pygame.time.Clock().tick(FPS)


def GameLoop():
	oTetrisTest = CTetrisTest.GetInstance()


class CBlock(object):
	def __init__(self):
		self.m_iFillList = []

	def InitFillList(self):
		pass

	def CheckRotate(self):
		return True

	def Rotate(self):
		pass


class CBlock_O(CBlock):
	def InitFillList(self):
		self.m_iFillList = []



class CTetrisTest(object):
	oInstance = None

	@classmethod
	def GetInstance(cls):
		if not cls.oInstance:
			cls.oInstance = CTetrisTest()
		return cls.oInstance

	def __init__(self):
		self.m_iGroundFillList = [0] * GROUND_GRID_SIZE[0] * GROUND_GRID_SIZE[1]
		self.Init()

	def Init(self):
		self.InitGround()

	def InitGround(self):
		iCol, iRow = GROUND_GRID_SIZE
		iLength = BLOCK_EDGE_LENGTH
		iWidth, iHeight = GROUND_SIZE

		iStartY = 0
		iEndY = iHeight
		for iIndex in xrange(iCol):
			if iIndex == 0:
				continue
			iX = iIndex * iLength + iIndex
			pygame.draw.line(g_oDisPlay, (125, 125, 125), (iX, iStartY), (iX, iEndY))

		iStartX = 0
		iEndX = iWidth
		for iIndex in xrange(iRow):
			if iIndex == 0:
				continue
			iY = iIndex * iLength + iIndex
			pygame.draw.line(g_oDisPlay, (125, 125, 125), (iStartX, iY), (iEndX, iY))

	def SpwanBlock(self, iBlockType):
		# oRect = pygame.Rect(0, 0, BLOCK_EDGE_LENGTH, BLOCK_EDGE_LENGTH)
		# print oRect, pygame.draw.rect(g_oDisPlay, (255, 255, 255), oRect)
		pass



if __name__ == "__main__":
	Main()
