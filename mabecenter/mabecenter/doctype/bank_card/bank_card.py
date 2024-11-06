# Copyright (c) 2024, Dante Devenir and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class BankCard(Document):
	
	def autoname(self):
		# Tomamos el nombre y los últimos 4 dígitos del número de tarjeta
		formatted_number = '-'.join([self.card_number[i:i+4] for i in range(0, len(self.card_number), 4)])

		# Generamos el nuevo nombre del Doctype con el formato deseado
		self.name = formatted_number
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from frappe.model.document import Document
from frappe.utils import comma_and, get_link_to_form


class BankCard(Document):
	def onload(self):
		load_address_and_contact(self)
  
	def autoname(self):
		# Tomamos el nombre y los últimos 4 dígitos del número de tarjeta
		formatted_number = '-'.join([self.card_number[i:i+4] for i in range(0, len(self.card_number), 4)])

		# Generamos el nuevo nombre del Doctype con el formato deseado
		self.name = formatted_number

	def on_trash(self):
		delete_contact_and_address("BankCard", self.name)