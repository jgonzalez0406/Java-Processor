import javalang


class CodeManager:
    def get_method_decl(self, snippet):
        tree = javalang.parse.parse(snippet) #goes through the javafile! makes it all possible
        names = list()

        #node: part of an imaginary tree
        for _, node in tree: #_ equates to throwaway. Auto deletes part of the code that isn't needed
            if isinstance(node, javalang.tree.MethodDeclaration):
                method_name = node.name
                names.append(method_name) #saves the name of methods to a list

        return names

    def get_method_text(self, startpos, endpos, startline, endline, last_endline_index, codelines):
        # thanks to https://github.com/c2nes/javalang/issues/49
        if startpos is None:
            return "", None, None, None
        else:
            startline_index = startline - 1
            endline_index = endline - 1 if endpos is not None else None

            # 1. check for and fetch annotations
            if last_endline_index is not None:
                for line in codelines[(last_endline_index + 1):(startline_index)]:
                    if "@" in line:
                        startline_index = startline_index - 1

            meth_text = "<ST>".join(codelines[startline_index:endline_index])
            meth_text = meth_text[:meth_text.rfind("}") + 1]

            # 2. remove trailing rbrace for last methods & any external content/comments
            if endpos is None and abs(meth_text.count("}") - meth_text.count("{")) == 0:
                # imbalanced braces
                brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

                for _ in range(brace_diff):
                    meth_text = meth_text[:meth_text.rfind("}")]
                    meth_text = meth_text[:meth_text.rfind("}") + 1]

            meth_lines = meth_text.split("<ST>")
            meth_text = "\n".join(meth_lines)
            last_endline_index = startline_index + (len(meth_lines) - 1)

            meth_lines = meth_text.split("<ST>")
            meth_text = "\n".join(meth_lines)
            last_endline_index = startline_index + (len(meth_lines) - 1)

            return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index
    def get_method_start_end(self, method_node,tree):
        # thanks to https://github.com/c2nes/javalang/issues/49
        startpos  = None
        endpos    = None
        startline = None
        endline   = None
        for path, node in tree:
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None
        return startpos, endpos, startline, endline

    def get_method_code(self, method, snippet):
        codelines = snippet.split('\n')
        tree = javalang.parse.parse(snippet)
        lex = None
        #method_texts = []

        # TODO: update this to work for overloaded methods
        # right now it will only return the first method of the given name
        for _, node in tree:
            if isinstance(node, javalang.tree.MethodDeclaration):
                if node.name == method:
                    method_node = node
                    #print(node.name)

                    startpos, endpos, startline, endline = self.get_method_start_end(method_node,tree)
                    method_text, startline, endline, lex = self.get_method_text(startpos, endpos, startline, endline, lex, codelines)
                   # method_texts.append((method_text, method_node))
                    return method_text
        return None

    def get_method_comments(self,method_name, java_code):
        method_start = java_code.find(method_name)
        method_end = java_code.find("}", method_start)

    # Search for the previous Javadoc comment block
        prev_comment_start = java_code.rfind("/**", 0, method_start)
        if prev_comment_start != -1:
            prev_comment_end = java_code.find("*/", prev_comment_start, method_start)
            if prev_comment_end != -1:
                javadoc_comment = java_code[prev_comment_start:prev_comment_end + 2]
                javadoc_comment_lines = javadoc_comment.strip().split("\n")
                formatted_javadoc_comment = "\n".join(["/**"] + [" * " + line.strip("/* ").strip() for line in javadoc_comment_lines[1:-1]] + [" */"])
                return formatted_javadoc_comment
        else:
            return ""
