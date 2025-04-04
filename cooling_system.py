"""
import random
random.seed(123)
from transport import transport

def cooling_system(env, name, mf, assembly_time, main_assembly_time, components_store, transport_time):

    max_retries = 3  # Retry limit in case of failure
    retries = 0
    
    # Request access to main factory
    print(f'{name}: All cooling system components arrive at time {round(env.now)}')
    
    while retries < max_retries:  # Retry on failure
        # Simulate manufacturing time
        yield env.timeout(assembly_time)
        
        # Simulate 10% failure probability
        if random.random() < 0.1:
            print(f'{name}: Manufacturing failure. Restarting... (Attempt {retries + 1})')
            retries += 1
            continue  # Restart manufacturing process
        
        # Continue if successful
        break  # Exit loop if no failure
    else:
        print(f'{name}: Critical failure. Could not manufacture cooling system.')
        return  # Exit if retry limit exceeded

    with mf.request() as req:
        yield req
        
        # Simulate main factory assembly time
        print(f'{name}: Starts cooling system manufacturing at time {round(env.now)}')
        yield env.timeout(main_assembly_time)
        print(f'{name}: Finishes assembly at time {round(env.now)}')
        
        # Simulate transport to main factory
        arrival = yield env.process(transport(env, transport_time))
        delay = arrival - env.now + transport_time  # Calculate delay
        print(f'{name}: Arrived at Main Factory at time {arrival} (Delay: {delay:.2f})')
        
        
        
        # Check for duplicates in store
        if 'CoolingSystem' not in components_store.items:
            yield components_store.put('CoolingSystem')
            print(f'{name}: CoolingSystem sent to component store at time {round(env.now, 2)}')
        else:
            print(f'{name}: Duplicate CoolingSystem. Ignoring...')
"""
import random
random.seed(123)
from transport import transport

def cooling_system(env, name, mf, assembly_time, main_assembly_time, components_store, transport_time):
    """
    Simulates the manufacturing and transportation of a processor.
    :param env: Simulation environment.
    :param name: Name of the processor.
    :param mf: Main factory resource.
    :param assembly_time: Manufacturing time.
    :param main_assembly_time: Assembly time at the main factory.
    :param components_store: Components store.
    :param transport_time: Transport time to the main factory.
    """
    max_retries = 3  # Retry limit in case of failure
    retries = 0

    # Component arrival message BEFORE any errors
    print(f'{name}: All cooling system components arrive at time {round(env.now)}')  

    while retries < max_retries:  # Retry on failure
        # Simulate manufacturing time
        yield env.timeout(assembly_time)
        
        # Simulate a 10% chance of failure
        if random.random() < 0.1:  
            print(f'{name}: Manufacturing failure. Restarting... (Attempt {retries + 1})')
            retries += 1
            continue  # Restart manufacturing process
        
        # If no failure, proceed
        break  # Exit loop if successful
    else:
        print(f'{name}: Critical failure. Could not manufacture the cooling system.')
        return  # Exit if retry limit exceeded

    # Request access to the main factory
    with mf.request() as req:
        yield req
        
        # Simulate assembly time at the main factory
        print(f'{name}: Starts cooling system manufacturing at time {round(env.now)}')
        yield env.timeout(main_assembly_time)
        print(f'{name}: Finishes assembly at time {round(env.now)}')
        
        # Simulate transport to the main factory
        arrival = yield env.process(transport(env, transport_time))
        delay = arrival - env.now + transport_time  # Calculate delay
        print(f'{name}: Arrived at Main Factory at time {arrival} (Delay: {delay:.2f})')
        
        # Check for duplicates
        if 'CoolingSystem' not in components_store.items:
            yield components_store.put('CoolingSystem')
            print(f'{name}: Cooling system sent to warehouse at time {round(env.now, 2)}')
        else:
            print(f'{name}: Duplicate processor. Ignoring...')