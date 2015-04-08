import Neverwherebot.models as models
import Neverwherebot.update
import random
import os

#####################################################################################
#	This Script contains all the different jobs you can have when you work on a farm. 
#	Current jobs: tilling, harvesting, planting, burning
#
#	Things to do:
#	- Calucate harvested amount
#	- Setting the right return values
#####################################################################################

def update(character, employment, hour):
	random.seed()
	override = check_upgrades("on_start", employment, character)

	#check if called at the right conditions
	if hour in [15,11] and employment.current_activity == "" and not override:
		if not employment.job.name == "farmer":
			print ("Farmer.py update called without the employee being a farmer, what's up with that?")
			return false

		override = check_upgrades("on_farm", employment, character)

	#setting basic variables
		if not override:
			for acre in models.Acre.objects.filter(farm=employment.worksite):
				if not models.Tending.objects.filter(day=Neverwherebot.update.get_current_day()).filter(acre=acre).exists():
					if employment.take_10:
						roll = Neverwherebot.update.get_skill(charakter, "farming") + 10
					else:
						roll = Neverwherebot.update.get_skill(charakter, "farming") + random.randint(1,20)

					today = models.Tending()
					today.worksite = employment.worksite
					today.day = Neverwherebot.update.get_current_day()
					today.roll = roll
					today.acre = acre
					today.save()

					check_upgrades("on_tend", employment, character, today)

			Neverwherebot.update.give_salary(character, employment.part, hour)
			return true

	#looking for job to call as function
		if hour in range(8,16):
			if employment.current_activity == "tilling" and not override:
				override = check_upgrades("on_till", employment, character)
				if not override:
					tilling(character, employment, hour, False)

			elif employment.current_activity == "tilling_all" and not override:
				override = check_upgrades("on_till", employment, character)
				if not override:
					tilling(character, employment, hour, True)

			elif employment.current_activity == "harvesting"  and not override:
				override = check_upgrades("on_harvest", employment, character)
				if not override:
					harvesting(character, employment, hour, False)

			elif employment.current_activity == "harvesting_all" and not override:
				override = check_upgrades("on_harvest", employment, character)
				if not override:
					harvesting(character, employment, hour, True)

			elif employment.current_activity == "planting" and not override:
				override = check_upgrades("on_plant", employment, character)
				if not override:
					planting(character, employment, hour, False)

			elif employment.current_activity == "planting_all" and not override:
				override = check_upgrades("on_plant", employment, character)
				if not override:
					planting(character, employment, hour, True)

			elif employment.current_activity == "burning" and not override:
				overide = check_upgrades("on_burn", employment)
				if not override:
					burning(character, employment, hour, False)
			else:
				print ("Farmer.py update called with the employee being a farmer but with no valid job, what's up with that?")
				return false


def tilling(character, employment, hour, all):
	if employment.acre is not None:
		done = false
		acre = employment.acre

	#Tilling acre
		if acre.tilled < 160:
			acre.tilled += 1
			acre.save()
			done = true

	#End of workday
			if hour == 15:
				if acre.tilled >= 160:
					message = "Todyay you finished tilling acre %s." % (acre.id)
				else:
					message = "Today, you worked on tilling acre %s, but you think around %i more man-days are necessary." % (acre.id, (160 - acre.tilling) / 8)

				Neverwherebot.update.send_message("", character.name, message, "bw")
				Neverwherebot.update.give_salary(character, employment.part, hour)
				return None

	#Acre is completly tilled
			if acre.tilled >= 160:
				message = "You finished tilling acre %s" % (acre.id)

				if all == False:
					employment.acre = None
					employment.current_activity = ""
					employment.save()
				else:
	#Looking for another acre that is available for tilling
					acre_found = False
					for a in models.Acre.objects.filter(worksite = employment.worksite):
						if a.tilled < 160:
							employment.acre = a
							employment.save()

							acre_found = True
							break
		
	#Handling of finding an acre or not
					if acre_found == False:
						message += ", you have been set back to idle activity."
						employment.acre = None
						employment.current_activity = ""
						employment.save()
					else:
						message += ", you have moved on to work on acre %s" % (a.id)
						if done == false:	#Tilling if not already tilled an acre
							employment.acre.tilled += 1
							employment.acre.save()

				Neverwherebot.update.send_message("", character.name, message, "bw")
				Neverwherebot.update.give_salary(character, employment.part, hour)
				return None

	#"Errorhandling"
		else:
			message = "Acre already tilled, you have been set back to idle activity."
			employment.acre = None
			employment.current_activity = ""
			employment.save()
			Neverwherebot.update.send_message("", character.name, message, "bw")
			return None
	else:
		message = "Having nothing to till, you have been set back to idle activity."
		employment.current_activity = ""
		employment.save()
		Neverwherebot.update.send_message("", character.name, message, "bw")
		return None

	#Paying worker
	Neverwherebot.update.give_salary(character, employment.part, hour)
	return None



def harvesting(employment, character, hour, all):
	if employment.acre is not None:
		done = false
		acre = employment.acre
		crop = employment.acre.crop
		worksite = employment.worksite
		
	#Harvesting acre
		if acre.produce > 0:
			if acre.produce >= acre.harvest_per:
				Neverwherebot.update.add_item(crop.product_name, sorage_id = worksite.storage.pk, amount=acre.harvest_per)
				acre.produce -= acre.harvest_per
			else:
				Neverwherebot.update.add_item(crop.product_name, storage_id = worksite.storage.pk, amount = acre.produce)
				acre.produce = 0
			
			acre.save()
			done = true

	#End of workday
			if hour == 15:
				if acre.produce == 0:
					message = "Today, you finished harvesting acre %s." % (acre.id)
				else:
					if employment.part == 0:
						amount = acre.harvest_per * 8
					else:
						amount = acre.harvest_per * 4

					message = "Today, you harvested %ikg of %s from acre %s, leaving roughly %ikg for harvesting" % (amount, crop.product_name, acre.id, acre.produce)
				
				Neverwherebot.update.send_message("", character.name, message, "bw")
				Neverwherebot.update.give_salary(character, employment.part, hour)
				return None

	#Acre completely harvested
		if acre.produce == 0:
			message = "Today, you harvested %ikg of %s from acre %s, harvesting the acre completed. " % (acre.produce, crop.product_name, acre.id)

			if not crop.perennial:
				acre.crop = None
				acre.planted = None

			acre.produce = 0
			acre.tilled = 0
			acre.harvest_per = 0
			acre.bonus = 0
			acre.growth_days = 0
			acre.save()

			if all == false:
				message += "You have been set back to idle." % (acre.id)
				employment.current_activity = ""
				employment.acre = None
				employment.save()
			else:
	#Looking for another acre that is available for harvesting
				for a in models.Acre.objects.filter(worksite=worksite):
					if a.produce > 0:
						employment.acre = a
						employment.save()
						break

				if employment.acre.produce > 0:
					message += "You started harvesting on acre %s." % (a.id)

					if done == false:
						if employment.acre.produce >= employment.acre.harvest_per:
							Neverwherebot.update.add_item(crop.product_name, storage_id = worksite.storage.pk, amount=employment.acre.harvest_per)
							employment.acre.produce -= employment.acre.harvest_per
						else:
							Neverwherebot.update.add_item(crop.product_name, storage_id = worksite.storage.pk, amount = employment.acre.produce)
							employment.acre.produce = 0
			
						employment.acre.save()
				else:
					message += "You have been set back to idle." % (acre.id)
				
			Neverwherebot.update.send_message("", character.name, message, "bw")
			Neverwherebot.update.give_salary(character, employment.part, hour)
			return None
	#"Errorhandeling"
		else:
			message = "Acre %s already harvested, you have been set back to idle." % (acre.id)
			employment.current_activity = ""
			employment.acre = None
			employment.save()
			Neverwherebot.update.send_message("", character.name, message, "bw")
			return None
	else:
		message = "Having nothing to harvest, you have been set back to idle."
		employment.current_activity = ""
		employment.save()
		Neverwherebot.update.send_message("", character.name, message, "bw")
		return None

	#Paying worker
	Neverwherebot.update.give_salary(character, employment.part, hour)
	return None



def planting(character, employment, hour, all):
	if employment.acre is not None:
		acre = employment.acre
		worksite = employment.worksite
		done = false

	#Planting Acre
		if acre.planting < 8:
			if acre.planting == 0:
				if start_planting(employment):
					message2 = "You began planting on acre %s." % (acre.id)
					Neverwherebot.update.send_message("", character.name, message2, "bw")
					done = true
				else:
					message2 = "You wanted to start planting on acre %s, but you could not find sufficient seed to do so and have been set back to idle." % (acre.id)
					Neverwherebot.update.send_message("", character.name, message2, "bw")

					employment.current_activity = ""
					employment.acre = None
					employment. save()
					return None
			else:
				acre.planting += 1
				acre.save()

	#End of Workday
			if hour == 15:
				if acre.planting == 8:
					message = "You finished planting %s on acre %s." % (acre.crop, acre.id)
				else:
					message = "You spent most of today planting %s on acre %s, but you have yet to finish." % (acre.crop, acre.id)

				Neverwherebot.update.send_message("", character.name, message, "bw")
				Neverwherebot.update.give_salary(character, employment.part, hour)
				return None

	#Finished Planting
			if acre. planting == 8:
				message = "You have finished planting %s on acre %s. " % (acre.crop, acre.id)
				acre.planted = Neverwherebot.update.get_current_day()
				acre.save()

				if all == False:
					message += "You have been set back to idle activity." 
					
					employment.acre = None
					employment.current_activity = ""
					employment.save()
				else:
	#Looking for another acre that is available for planting
					for a in models.Acre.objects.filter(worksite=worksite):
						if a.planting < 8:
							employment.acre = a
							employment.save()
							break

					if employment.acre.planting == 8:
						message += "But you couldn't find another acre, you have been set back to idle activity."
						employment.acre = None
						employment.current_activity = ""
						employment.save()
					else:
						message += "You moved on to acre %s." % (a.id)

						if done == false:
							if acre.planting == 0:
								if start_planting(employment):
									message2 = "You began planting on acre %s." % (acre.id)
									Neverwherebot.update.send_message("", character.name, message2, "bw")
									done = true
								else:
									message2 = "You wanted to start planting on acre %s, but you could not find sufficient seed to do so and have been set back to idle." % (acre.id)
									Neverwherebot.update.send_message("", character.name, message2, "bw")

									employment.current_activity = ""
									employment.acre = None
									employment. save()
									return None
							else:
								acre.planting += 1
								acre.save()

				Neverwherebot.update.send_message("", character.name, message, "bw")
				Neverwherebot.update.give_salary(character, employment.part, hour)
				return None

	#"Errorhandling"
		else:
			message = "Nothing to plant on acre %s, you have been set back to idle activity." % (acre.id)
			employment.acre = None
			employment.current_activity = ""
			employment.save()
			Neverwherebot.update.send_message("", character.name, message, "bw")
			return None
	else:
		message = "No acre found for planting, you have been set back to idle activity."
		employment.current_activity = ""
		employment.save()
		Neverwherebot.update.send_message("", character.name, message, "bw")
		return None

	#Paying Worker
	Neverwherebot.update.give_salary(character, employment.part, hour)
	return None

					

def burning(character, employment, hour, all):
	if employment.acre is not None:
		acre = employment.acre
		if acre.crop is not None:
	#Burning acre
			acre.reset()
			if acre.fertility == "Barren":
				acre.fertility = "Bad"
			elif acre.fertility == "Bad":
				acre.fertility = "Normal"

			acre.save()

			message = "You burnt the acre %s to the ground." % (acre.id)
		else:
			message = "You wanted to burn the acre %s, but there was nothing there worth burning." % (acre.id)

		employment.current_activity = ""
		employment.acre = None
		employment.save()
		Neverwherebot.update.sent_message("",charater.name, message, "bw")
		Neverwherebot.update.give_salary(character, employment.part, hour)
		return None

	#"Errorhandling"
	else:
		message = "No acre found for burning, you have been set back to idle activity."
		employment.current_activity = ""
		employment.save()
		Neverwherebot.update.send_message("", character.name, message, "bw")
		return None


def check_upgrades(function, employment, *args):
    if models.Upgrade.objects.filter(worksite=employment.worksite).exists():
        for upgrade in models.Upgrade.objects.filter(worksite=employment.worksite):
            result = Neverwherebot.update.exec_script(os.path.join("worksites", "farm", "upgrades"), upgrade.type.name, function, *args)
            if result == "override":
                return True
            else:
                return False
    return False


def start_planting(employment):
    character = employment.character
    acre = employment.acre
    crop_name = employment.current_activity[13:]  # Strip away "planting_all "						WHAT IF NOT PLANTING_ALL OR ANOTHER JOB!!!!!!!!!!!!!

	#Checking if crop exists
    try:
        crop = models.Crop.objects.get(name=crop_name)
    except:
        return False

    seed = crop.seed_type
    worksite = employment.worksite
    storage = worksite.storage

	#Checking for seeds in worksite iventory
    if Neverwherebot.update.is_item(seed.name, storage_id=storage.pk, amount=crop.seed):
        Neverwherebot.update.remove_item(seed.name, storage_id=storage.pk, amount=crop.seed)
        acre.crop = crop
        acre.planting = 1
        acre.planted = Neverwherebot.update.get_current_day()
        acre.save()
        return True

	#Checking for seeds in player inventory
    elif Neverwherebot.update.is_item(seed.name, storage_id=character.inventory.pk, amount=crop.seed):
        Neverwherebot.update.remove_item(seed.name, storage_id=character.inventory.pk, amount=crop.seed)
        acre.crop = crop
        acre.planting = 1
        acre.planted = Neverwherebot.update.get_current_day()
        acre.save()
        return True

	return None
