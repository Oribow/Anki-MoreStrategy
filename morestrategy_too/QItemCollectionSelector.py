'''
Created on Dec 16, 2017

@author: Oribow
'''
from PyQt5.Qt import  \
    QMenu, QTableView
from PyQt5.QtCore import Qt, pyqtSignal, QAbstractTableModel, QModelIndex, QVariant, QSortFilterProxyModel, QObject
from data.StrUtil import tStr
from data import StrUtil, ItemTemplates
from morestrategy_too.AmountList import AmountList, AmountItem
from data.Refila import ItemFilterJoin


class QItemCollectionSelector(QObject):
    selectedChanged = pyqtSignal(AmountItem)

    def __init__(self, tableView, actor, allowContext):
        QObject.__init__(self)
        self.actor = actor
        actor.ownedItems.aItemChanged.connect(self.actorsItemsChanged)
        self.preFilter = None
        self.filter = None
        # table
        self.tableView = tableView
        self.tableView.setSortingEnabled(True)
        self.tableView.selectionChanged = self.selectedItemChanged
        self.tableModel = ItemTableModel(self.actor.ownedItems)
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.tableModel)
        self.proxyModel.setSortRole(Qt.EditRole)
        self.tableView.setModel(self.proxyModel)
        resizeColumns(self.tableView, self.tableModel.columnCount())
        # bunch func exec
        if allowContext:
            self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableView.customContextMenuRequested.connect(self.itemTableViewContextMenu)
            self.cachedFuncs = None
            self.cachedIndex = None

    def setConstantPreFilter(self, preFilter):
        self.preFilter = preFilter
        self.updateFilter(self.filter)

    def getCurrentSelected(self):
        index = self.proxyModel.mapToSource(self.tableView.selectionModel().currentIndex())
        if not index.isValid():
            return AmountItem(None, None)
        return self.tableModel.filteredAItemList[index.row()]

    def actorsItemsChanged(self, batch):
        if batch[0] == AmountList.CHANGE_COMPLETELY:
            self.tableModel.reapplyFilter()
            return
        for i in batch:
            code = i[1]
            aItem = i[0]
            if code == AmountList.CHANGE_AMOUNT:
                #dataChanged
                i = self.tableModel.filteredAItemList.getIndexById(aItem.item.id)
                if i is None:
                    continue
                index = self.tableModel.index(i, 0)
                self.tableModel.dataChanged.emit(index, index)
            elif code == AmountList.CHANGE_REMOVED:
                i = self.tableModel.filteredAItemList.getIndexById(aItem.item.id)
                if i == None:
                    continue
                self.tableModel.layoutAboutToBeChanged.emit()
                del self.tableModel.filteredAItemList.aItemList[i]
                self.tableModel.layoutChanged.emit()
            elif code == AmountList.CHANGE_APPEND:
                if not self.tableModel.cachedFilter.isValidItem(aItem):
                    continue
                self.tableModel.layoutAboutToBeChanged.emit()
                self.tableModel.filteredAItemList.append(aItem)
                self.tableModel.layoutChanged.emit()


    def itemTableViewContextMenu(self, pos):
        menu = QMenu()
        funcs = self.getFuncsAllSelectedItemsHave()
        if funcs == None:
            return
        for k, v in funcs.iteritems():
            menu.addAction(tStr(k), lambda func=v: func(self.getCurrentSelected(), self.actor))

        menu.exec_(self.tableView.mapToGlobal(pos))

    def getFuncsAllSelectedItemsHave(self):
        index = self.tableView.selectedIndexes()
        if index == self.cachedIndex:
            return self.cachedFuncs

        if len(index) == 0:
            return None

        funcs = {}
        for i in index:
            f = self.getCurrentSelected().item.getExtraFunctionality()
            if funcs == {}:
                funcs = f
            else:
                newFuncs = {}
                for k in funcs.iterkeys():
                    if k in f:
                        newFuncs[k] = f[k]
                funcs = newFuncs

        self.cachedIndex = index
        self.cachedFuncs = funcs
        return funcs

    def updateFilter(self, filter):
        self.filter = filter
        if self.preFilter != None:
            if filter == None:
                filter = self.preFilter
            else:
                filter = ItemFilterJoin(self.preFilter, ItemFilterJoin.AND, filter)
        self.tableModel.setFilter(filter)

    def selectedItemChanged(self, selected, deselected):
        QTableView.selectionChanged(self.tableView, selected, deselected)
        self.selectedChanged.emit(self.getCurrentSelected())

    def resizeColumns(self):
        resizeColumns(self.tableView, self.tableModel.columnCount())


class ItemTableModel(QAbstractTableModel):

    def __init__(self, aItemList):
        QAbstractTableModel.__init__(self)
        self.aItemList = aItemList
        self.filteredAItemList = AmountList(list(aItemList.aItemList))
        self.setFilter(None)
        self.cachedFilter = None

    def setFilter(self, filter):
        self.cachedFilter = filter
        self.beginResetModel()
        if filter == None:
            self.filteredAItemList.aItemList = list(self.aItemList.aItemList)
        else:
            self.filteredAItemList.aItemList = []
            for i in self.aItemList:
                if filter.isValidItem(i):
                    self.filteredAItemList.aItemList.append(i)

        self.updateColumns()
        self.endResetModel()

    def reapplyFilter(self):
        self.setFilter(self.cachedFilter)

    def rowCount(self, index=QModelIndex()):
        return len(self.filteredAItemList)

    def columnCount(self, index=QModelIndex()):
        return len(self.columns)

    def updateColumns(self):
        types = []
        for i in self.filteredAItemList:
            if not type(i.item) in types:
                types.append(type(i.item))

        self.columns = None
        for t in types:
            attrs = t.getAttrsForTable()
            if self.columns == None:
                self.columns = attrs
                continue

            new_list = [a for a in self.columns if a in attrs]
            self.columns = new_list

        if self.columns == None:
            self.columns = [StrUtil.ITEM_ATTR_AMOUNT]
        else:
            self.columns.insert(0, StrUtil.ITEM_ATTR_AMOUNT)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))
        elif role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return tStr(self.columns[section])
            elif orientation == Qt.Vertical:
                return QVariant(section + 1)
        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
                (0 > index.row() < len(self.entities)):
            return QVariant()
        i = self.filteredAItemList[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return str(i.amount)
            return i.item.getData(self.columns[index.column()], ItemTemplates.DISPLAY_ROLE)
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
        elif role == Qt.EditRole:
            if index.column() == 0:
                return i.amount
            return i.item.getData(self.columns[index.column()], ItemTemplates.SORTING_ROLE)
        elif role == Qt.UserRole:
            return i
        return QVariant()


def resizeColumns(tableView, columnCount):
    for c in range(columnCount):
        tableView.resizeColumnToContents(c)
