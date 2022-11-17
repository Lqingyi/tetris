# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.locals import *

BLOCK_EDGE_LENGTH = 30
GROUND_GRID_SIZE = 10, 20
GROUND_SIZE = BLOCK_EDGE_LENGTH * GROUND_GRID_SIZE[0], BLOCK_EDGE_LENGTH * GROUND_GRID_SIZE[1]
FPS = 60

g_oSurface = None
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
	global g_oSurface
	pygame.init()
	g_oSurface = pygame.display.set_mode(size=GROUND_SIZE)
	pygame.display.set_caption("tetris")


def Loop():
	while True:
		GameLoop()
		pygame.display.update()
		pygame.time.Clock().tick(FPS)


def GameLoop():
	ProcessEvent()
	Draw()


def ExitGame():
	pygame.quit()
	sys.exit()


def ProcessEvent():
	if pygame.event.get(pygame.QUIT):
		ExitGame()

	oTetrisTest = CTetrisTest.GetInstance()
	for oEvent in pygame.event.get(pygame.KEYDOWN):
		sKey = pygame.key.name(oEvent.key)
		if sKey == "down":
			oTetrisTest.FallBlock()
		elif sKey == "up":
			oTetrisTest.FallBlock(bToBottom=True)
		elif sKey == "left":
			oTetrisTest.RotateBlock(False)
		elif sKey == "right":
			oTetrisTest.RotateBlock(True)
		elif sKey == "escape":
			ExitGame()


def Draw():
	oTetrisTest = CTetrisTest.GetInstance()
	oTetrisTest.Draw()


def MatrixMulti(mR, mV):
	iResultList = []
	for tRow in mR:
		iResultList.append(sum(map(lambda t: t[0] * t[1], zip(tRow, mV))))
	return iResultList


class CBlock(object):
	BLOCK_TYPE_T = "T"
	BLOCK_TYPE_I = "I"

	BLOCK_TYPE_2_POINTS = {
		BLOCK_TYPE_T: (
			((3, 21), (4, 21), (5, 21), (4, 22)),
			(4, 21)
		),

		BLOCK_TYPE_I: (
			((3, 22), (4, 22), (5, 22), (6, 22)),
			(4.5, 22.5)
		),
	}

	def __init__(self):
		self.m_sType = ""
		self.m_lPointList = []
		self.m_lRotatePoint = []

	def SetType(self, sType):
		dType2Points = CBlock.BLOCK_TYPE_2_POINTS
		if sType not in dType2Points:
			raise ValueError("sType:%s" % (sType,))
		self.m_sType = sType
		tPoints = dType2Points[sType]
		self.UpdatePoints([list(t) for t in tPoints[0]], lRotatePoint=list(tPoints[1]))

	def UpdatePoints(self, lPointList, lRotatePoint=None):
		self.m_lPointList = lPointList
		if lRotatePoint:
			self.m_lRotatePoint = lRotatePoint

	def GetPointList(self):
		return self.m_lPointList

	def GetRotatePoint(self):
		return self.m_lRotatePoint


class CTetrisTest(object):
	oInstance = None

	@classmethod
	def GetInstance(cls):
		if not cls.oInstance:
			cls.oInstance = CTetrisTest()
		return cls.oInstance

	def __init__(self):
		self.m_iGroundPointList = [0] * GROUND_GRID_SIZE[0] * GROUND_GRID_SIZE[1]
		self.m_oBlock = CBlock()
		self.Init()

	def Init(self):
		#self.InitGround()
		self.SpwanBlock(CBlock.BLOCK_TYPE_I)

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
			pygame.draw.line(g_oSurface, (125, 125, 125), (iX, iStartY), (iX, iEndY))

		iStartX = 0
		iEndX = iWidth
		for iIndex in xrange(iRow):
			if iIndex == 0:
				continue
			iY = iIndex * iLength + iIndex
			pygame.draw.line(g_oSurface, (125, 125, 125), (iStartX, iY), (iEndX, iY))

	def Draw(self):
		g_oSurface.fill((0, 0, 0))
		# 绘制已经固定的block

		# 绘制当前活动方块
		oBlock = self.m_oBlock
		iOffset = BLOCK_EDGE_LENGTH * 0.5
		iGroundH = GROUND_SIZE[1]
		for lPoint in oBlock.GetPointList():
			iCol, iRow = lPoint
			oRect = pygame.Rect(
				iCol * BLOCK_EDGE_LENGTH,
				iGroundH - (iRow + 1) * BLOCK_EDGE_LENGTH,
				BLOCK_EDGE_LENGTH,
				BLOCK_EDGE_LENGTH,
			)
			pygame.draw.rect(g_oSurface, (255, 255, 255), oRect)

	def CheckValid(self, lPointList):
		iGroundPointList = self.m_iGroundPointList
		iGroundGridW, iGroundGridH = GROUND_GRID_SIZE
		for iCol, iRow in lPointList:
			if not (0 <= iCol < iGroundGridW and iRow > 0):
				print "return False area", iCol, iRow
				return False
			if iRow >= iGroundGridH:
				print "return False H", iRow
				continue
			if iGroundPointList[int(iRow * iGroundGridW + iCol)]:
				print "has block"
				return False
		return True

	def SpwanBlock(self, sBlockType):
		self.m_oBlock.SetType(sBlockType)

	def RotateBlock(self, bClockwise):
		oBlock = self.m_oBlock
		fRX, fRY = oBlock.GetRotatePoint()
		if bClockwise:
			m = (
				(0, 1, fRX - fRY),
				(-1, 0, fRX + fRY),
				(0, 0, 1),
			)
		else:
			m = (
				(0, -1, fRX + fRY),
				(1, 0, fRY - fRX),
				(0, 0, 1),
			)
		lPointList = []
		for iIndex, (iCol, iRow) in enumerate(oBlock.GetPointList()):
			iResultList = MatrixMulti(m, (iCol, iRow, 1))
			lPointList.append(iResultList[:2])
		print "RotateResult", lPointList
		if not self.CheckValid(lPointList):
			return
		oBlock.UpdatePoints(lPointList)

	def FallBlock(self, bToBottom=False):
		oBlock = self.m_oBlock
		iTryTimes = 1 if not bToBottom else (GROUND_GRID_SIZE[1] + 5)
		lRotatePoint = oBlock.GetRotatePoint()
		lPointList = [list(lPoint) for lPoint in oBlock.GetPointList()]
		bChanged = False
		while iTryTimes > 0:
			iTryTimes -= 1
			for lPoint in lPointList:
				lPoint[1] -= 1
			lRotatePoint[1] -= 1
			print "FallResult", lPointList
			if not self.CheckValid(lPointList):
				break
			bChanged = True
		if bChanged:
			oBlock.UpdatePoints(lPointList, lRotatePoint=lRotatePoint)


	def GetBlock(self):
		return self.m_oBlock


if __name__ == "__main__":
	Main()
