import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.program import TemplateProgramNode
from programy.bot import Bot, BotConfiguration
from programy.brain import Brain, BrainConfiguration

from programytest.parser.template.base import TemplateTestsBaseClass


class MockTemplateProgramNode(TemplateProgramNode):
    def __init__(self):
        TemplateProgramNode.__init__(self)

    def resolve_to_string(self, bot, clientid):
        raise Exception("This is an error")

class TemplateProgramNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateProgramNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        test_bot.brain.properties.add_property("fullname", "testbot")
        test_bot.brain.properties.add_property("version", "1.0.0")

        self.assertEqual(root.resolve(test_bot, "testid"), "testbot 1.0.0")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateProgramNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><program /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateProgramNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)