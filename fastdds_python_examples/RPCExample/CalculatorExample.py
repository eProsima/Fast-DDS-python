#!/usr/bin/env python3
# # Copyright 2025 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Script to test Fast DDS python bindings for RPC
"""
import os
import argparse
import threading
import time

import fastdds
import calculator

DESCRIPTION = """Calculator RPC example for Fast DDS python bindings"""
USAGE = ('python3 CalculatorExample.py -p client|server [-d domainID -t server_threads]')

### Server implementation ###

class MyCalculatorImplementation(calculator.CalculatorServerImplementation):
  def __init__(self):
    super().__init__()

  def operation_call_print(self, info, operation_name):
    print("Operation {op} called from client with id {id}".format(op=operation_name, id=info.get_client_id()))

  def addition(self, info, value1, value2):
    self.operation_call_print(info, "addition")
    return value1 + value2

  def subtraction(self, info, value1, value2):
    self.operation_call_print(info, "subtraction")
    return value1 - value2

  def representation_limits(self, info):
    self.operation_call_print(info, "representation_limits")
    ret_val = calculator.BasicCalculator_representation_limits_Out()
    ret_val.min_value = -2147483648
    ret_val.max_value = 2147483647
    return ret_val

  def fibonacci_seq(self, info, n_results, result_writer):
    self.operation_call_print(info, "fibonacci_seq")
    a = 1
    b = 1
    c = 0
    
    while n_results > 0:
      n_results = n_results - 1
      
      result_writer.write(a)
      c = a + b
      a = b
      b = c

  def sum_all(self, info, value):
    self.operation_call_print(info, "sum_all")
    ret = 0
    has_value, n = value.read()
    while has_value:
      ret = ret + n
      has_value, n = value.read()
    return ret

  def accumulator(self, info, value, result_writer):
    self.operation_call_print(info, "accumulator")
    ret = 0
    has_value, n = value.read()
    while has_value:
      ret = ret + n
      result_writer.write(ret)
      has_value, n = value.read()

### Server application ###

def run_server(server):
    server.run()

class Server:
  def __init__(self, domain, num_threads):
    # Create participant
    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(domain, self.participant_qos)

    # Create server
    self.implementation = MyCalculatorImplementation()
    self.server_qos = fastdds.ReplierQos()
    self.server = calculator.create_CalculatorServer(
      self.participant, "my_calculator", self.server_qos, num_threads, self.implementation)

  def run(self):
    thr = threading.Thread(target=run_server, args=(self.server,))
    thr.start()
    print("Server is running. Press any key to stop it.")
    try:
      input()
    except:
      pass
    self.server.stop()
    thr.join()

### Client application ###

class Client:
  def __init__(self, domain):
    # Create participant
    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(domain, self.participant_qos)

    # Create client
    self.client_qos = fastdds.RequesterQos()
    self.client = calculator.create_CalculatorClient(
      self.participant, "my_calculator", self.client_qos)

  def run(self):
    # TODO: wait for server to be ready
    time.sleep(2)

    self.perform_addition()
    self.perform_subtraction()
    self.perform_representation_limits()
    self.perform_fibonacci_seq()
    self.perform_sum_all()
    self.perform_accumulator()

  def perform_addition(self):
    try:
      # Perform basic addition
      print("Performing addition(1, 2)")
      result = self.client.addition(1, 2)
      print("Result: {}".format(result.get()))

      # Perform addition with overflow
      print("Performing addition(2147483647, 1)")
      result = self.client.addition(2147483647, 1)
      print("Result: {}".format(result=result.get()))
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

  def perform_subtraction(self):
    try:
      # Perform basic subtraction
      print("Performing subtraction(2, 1)")
      result = self.client.subtraction(2, 1)
      print("Result: {}".format(result.get()))

      # Perform subtraction with underflow
      print("Performing subtraction(-2147483648, 1)")
      result = self.client.subtraction(-2147483648, 1)
      result.wait()
      print("Result: {}".format(result=result.get()))
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

  def perform_representation_limits(self):
    try:
      # Perform representation limits
      print("Performing representation_limits()")
      result = self.client.representation_limits()
      data = result.get()
      print("Result: {min}, {max}".format(min=data.min_value, max=data.max_value))
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

  def perform_fibonacci_seq(self):
    try:
      print("Performing fibonacci_seq(10)")
      result = self.client.fibonacci_seq(10)
      has_value, n = result.read()
      while has_value:
        print("Result: {}".format(n))
        has_value, n = result.read()
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

  def perform_sum_all(self):
    try:
      print("Performing sum_all([1, 2, 3, 4, 5])")
      result, value = self.client.sum_all()
      value.write(1)
      value.write(2)
      value.write(3)
      value.write(4)
      value.write(5)
      value.finish()
      print("Result: {}".format(result.get()))
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

  def perform_accumulator(self):
    try:
      print("Performing accumulator([1, 2, 3, 4, 5])")
      result, value = self.client.accumulator()
      value.write(1)
      value.write(2)
      value.write(3)
      value.write(4)
      value.write(5)
      value.finish()
      has_value, n = result.read()
      while has_value:
        print("Result: {}".format(n))
        has_value, n = result.read()
    except Exception as e:
      print("Exception: {}".format(type(e).__name__))
      print("Exception message: {}".format(e))

def parse_options():
  """"
  Parse arguments.

  :return: Parsed arguments.
  """
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    add_help=True,
    description=(DESCRIPTION),
    usage=(USAGE)
  )
  required_args = parser.add_argument_group('required arguments')
  required_args.add_argument(
    '-d',
    '--domain',
    type=int,
    required=False,
    help='DomainID.'
  )
  required_args.add_argument(
    '-p',
    '--parameter',
    type=str,
    required=True,
    help='Whether the application is run as client or server.'
  )
  required_args.add_argument(
    '-t',
    '--server_threads',
    type=int,
    required=False,
    help='Number of threads in the server pool. Only applies if the application is run as server.'
  )
  return parser.parse_args()

if __name__ == '__main__':
  # Parse arguments
  args = parse_options()
  if not args.domain:
    args.domain = 0
  if not args.server_threads:
    args.server_threads = 1

  if args.parameter == 'client':
    print('Creating client.')
    client = Client(args.domain)
    client.run()
  elif args.parameter == 'server':
    print('Creating server.')
    server = Server(args.domain, args.server_threads)
    server.run()
  else:
    print('Error: Incorrect arguments.')
    print(USAGE)

  exit()
