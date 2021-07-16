(define (domain office)
  (:requirements   :strips  :typing  :negative-preconditions :disjunctive-preconditions :fluents :equality :conditional-effects)
  (:types
   room light fan humidifier  message  - object
   )
   
    (:predicates
         
          (comfortable-light)
          (comfortable-temperature)
          (comfortable-humidity)
          
          (off ?l - light)
          (off1 ?f - fan)
          (off2 ?h - humidifier)
          (at-light ?l - light  ?r - room)
          (at-fan ?f - fan ?r - room)
          (at-humidifier ?h - humidifier ?r - room)
          (send ?m - message)     
    )

   (:functions
    
	  (temp ?r - room )
	  (lightintensity ?r - room)
	  (humidity ?r - room)
	  (occupy ?r - room)
	  (temp_limit)
	  (temp1_limit)
      (humidity_limit)
      (lightintensity_limit)
      (occupy_limit)
   )

  ; automatic brightness control in the office


   
   (:action switchoff_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (and (off ?l) (>=(occupy ?r) (occupy_limit)) (<(lightintensity ?r) (lightintensity_limit)))
        :effect (and (not(off ?l)) (send ?m) (comfortable-light))
    )

    (:action switchon_light
        :parameters (?l - light ?r - room ?m - message)
        :precondition (and (off ?l) (>=(occupy ?r) (occupy_limit)) (>=(lightintensity ?r) (lightintensity_limit)))
        :effect (and (not(off ?l)) (send ?m) (comfortable-light))
    )
   
   (:action noperson_light_off
        :parameters (?l - light ?r - room ?m - message)
        :precondition (or (not(off ?l)) (<(occupy ?r) (occupy_limit)))
        :effect (and (off ?l) (send ?m) (comfortable-light))
    )

      

   
   
   ; automatic ventilator control in the office
   
   
     
       
   (:action switchoff_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (and (off1 ?f) (>=(occupy ?r) (occupy_limit)) (<(temp ?r) (temp_limit)))
        :effect (and(not(off1 ?f)) (send ?m) (comfortable-temperature))
   )
   
  
     
   (:action switchon_fan
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (and (off1 ?f) (>=(occupy ?r) (occupy_limit)) (>(temp ?r) (temp1_limit)))
        :effect (and (not(off1 ?f)) (send ?m) (comfortable-temperature))
   )
   
    
     
   (:action noperson_fan_off
        :parameters (?f - fan ?r - room ?m - message)
        :precondition (or (not(off1 ?f)) (<(occupy ?r) (occupy_limit)))
        :effect (and (off1 ?f) (send ?m) (comfortable-temperature))
    )



   ; automatic humidifer valve control in the office



    (:action switchoff_humidifier
        :parameters (?h - humidifier ?r - room ?m - message)
        :precondition (and (off2 ?h) (>=(occupy ?r) (occupy_limit)) (<(humidity ?r) (humidity_limit)))
        :effect (and(not(off2 ?h)) (send ?m) (comfortable-humidity))
     )
   
    (:action switchon_humidifier
        :parameters (?h - humidifier ?r - room ?m - message)
        :precondition (and (off2 ?h) (>=(occupy ?r) (occupy_limit)) (>(humidity ?r) (humidity_limit)))
        :effect (and (not(off2 ?h)) (send ?m) (comfortable-humidity))
     )
     
     
   (:action noperson_humidifier_off
        :parameters (?l - light ?r - room ?m - message)
        :precondition (or (not(off ?l)) (<(occupy ?r) (occupy_limit)))
        :effect (and (off ?l) (send ?m) (comfortable-humidity))
    )

)
