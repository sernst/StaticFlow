content = """\
[#box][#summary]This is a test of the[/#summary] [#b][#i]emergency[/#i] broadcast system[/#b]. In the event of an ->>
actual emergency...[/#box]
"""

from StaticFlow.render.MarkupProcessor import MarkupProcessor

p = MarkupProcessor(content, debug=True)
result = p.get()

print result
print 'Processing complete!'
