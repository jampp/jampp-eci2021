# delete all the cython generated files
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.so" -exec rm -rf {} \;
find . -name "*.pyo" -exec rm -rf {} \;

# rm -rf time_output.txt
. /home/vpaz/envs/eci-uba/bin/activate

# cd 1-python
# echo "etapa 1 - python" >> ../time_output.txt
# { time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

# cd ../2-c
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
#     -I/usr/include/python3.8 -o levenshtein.so levenshtein.c
# echo "etapa 2 - c" >> ../time_output.txt
# { time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

# cd ../3-cython
# cython difference.py
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
#     -I/usr/include/python3.8 -o difference.so difference.c
# echo "etapa 3 - cython SIN tipos" >> ../time_output.txt
# { time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

# cd ../3-cython-tipos
# cython difference.py
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
#     -I/usr/include/python3.8 -o difference.so difference.c
# echo "etapa 4 - cython CON tipos" >> ../time_output.txt
# { time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
# { time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

cd ../4-cython-muchos-tipos
cython difference.py
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
    -I/usr/include/python3.8 -o difference.so difference.c
echo "etapa 5 - cython MUCHOS tipos" >> ../time_output.txt
{ time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

cd ../5-cython-sin-limites
cython difference.py
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
    -I/usr/include/python3.8 -o difference.so difference.c
echo "etapa 5 - cython MUCHOS tipos + SIN bordes" >> ../time_output.txt
{ time python main.py ../dataset.1.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.3.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.7.txt ; } 2>> ../time_output.txt
{ time python main.py ../dataset.15.txt ; } 2>> ../time_output.txt

