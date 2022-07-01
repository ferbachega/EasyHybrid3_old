class SphereInstanceRepresentation (Representation):
    """ Class doc """
    
    def __init__ (self, name = 'SphereInstance', active = True, _type = 'mol', vobject = None, glCore = None, indexes = None):
        """ Class initialiser """
        self.name               = name
        self.active             = active
        self.type               = _type

        self.vobject             = vobject
        self.glCore             = glCore
        self.indexes            = indexes
        
        self.light_position = np.array([-2.5, 2.5, 3.0],dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_ambient_coef = 0.4
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6, 0.6, 0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0, 1.0, 1.0],dtype=np.float32)
        
        v_instances = """
        #version 330

        uniform mat4 model_mat;
        uniform mat4 view_mat;
        uniform mat4 proj_mat;

        in vec3 vert_coord;
        in vec3 vert_color;
        in vec3 vert_instance;
        in float vert_radius;

        vec3 vert_norm;

        out vec3 frag_coord;
        out vec3 frag_color;
        out vec3 frag_norm;

        void main(){
            mat4 modelview = view_mat * model_mat;
            vec3 offset_coord = vert_coord * vert_radius + vert_instance;
            gl_Position = proj_mat * modelview * vec4(offset_coord, 1.0);
            
            vert_norm = normalize(offset_coord - vert_instance);
            frag_coord = vec3(modelview * vec4(offset_coord, 1.0));
            frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
            frag_color = vert_color;
        }
        """
        f_instances = """
        #version 330

        struct Light {
           vec3 position;
           //vec3 color;
           vec3 intensity;
           //vec3 specular_color;
           float ambient_coef;
           float shininess;
        };

        uniform Light my_light;

        in vec3 frag_coord;
        in vec3 frag_color;
        in vec3 frag_norm;

        out vec4 final_color;

        vec4 calculate_color(vec3 fnrm, vec3 fcrd, vec3 fcol){
            vec3 normal = normalize(fnrm);
            vec3 vert_to_light = normalize(my_light.position);
            vec3 vert_to_cam = normalize(fcrd);
            // Ambient Component
            vec3 ambient = my_light.ambient_coef * fcol * my_light.intensity;
            // Diffuse component
            float diffuse_coef = max(0.0, dot(normal, vert_to_light));
            vec3 diffuse = diffuse_coef * fcol * my_light.intensity;
            // Specular component
            float specular_coef = 0.0;
            if (diffuse_coef > 0.0)
                specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(vert_to_light, normal))), my_light.shininess);
            vec3 specular = specular_coef * my_light.intensity;
            specular = specular * (vec3(1) - diffuse);
            vec4 out_color = vec4(ambient + diffuse + specular, 1.0);
            return out_color;
        }

        void main(){
            final_color = calculate_color(frag_norm, frag_coord, frag_color);
        }
        """


        self.gl_program_instances = self.load_shaders(v_instances, f_instances)
        self.instances_vao = None
        
        ## representation 	
        #self.vao            = None
        #self.ind_vbo        = None
        #self.coord_vbo      = None
        #self.col_vbo        = None
        #self.size_vbo       = None
        #   
        #
        ## bgrd selection   
        #self.sel_vao        = None
        #self.sel_ind_vbo    = None
        #self.sel_coord_vbo  = None
        #self.sel_col_vbo    = None
        #self.sel_size_vbo   = None
        #
        #
        ##     S H A D E R S
        #self.shader_program     = None
        #self.sel_shader_program = None


    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, "my_light.position")
        GL.glUniform3fv(light_pos, 1, self.light_position)
        #light_col = GL.glGetUniformLocation(program, "my_light.color")
        #GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, "my_light.ambient_coef")
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, "my_light.shininess")
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, "my_light.intensity")
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        #spec_col = GL.glGetUniformLocation(program, "my_light.specular_color")
        #GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        return True

    def load_shaders(self, vertex, fragment, geometry=None):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(vertex, GL.GL_VERTEX_SHADER)
        my_fragment_shader = self.create_shader(fragment, GL.GL_FRAGMENT_SHADER)
        if geometry is not None:
            my_geometry_shader = self.create_shader(geometry, GL.GL_GEOMETRY_SHADER)
        program = GL.glCreateProgram()
        GL.glAttachShader(program, my_vertex_shader)
        GL.glAttachShader(program, my_fragment_shader)
        if geometry is not None:
            GL.glAttachShader(program, my_geometry_shader)
        GL.glLinkProgram(program)
        return program
    
    def create_shader(self, shader_prog, shader_type):
        """ Creates, links to a source, compiles and returns a shader.
            
            Keyword arguments:
            shader -- The shader text to use
            shader_type -- The OpenGL enum type of shader, it can be:
                           GL.GL_VERTEX_SHADER, GL.GL_GEOMETRY_SHADER or GL.GL_FRAGMENT_SHADER
            
            Returns:
            A shader object identifier or pops out an error
        """
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, shader_prog)
        GL.glCompileShader(shader)
        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", shader_type)
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader

        
    def _make_gl_vao_and_vbos (self, program):
        ''' '''
        coords, indexes, colors = sphd.get_sphere([1,1,1], 1.0, [0, 1, 0], level="level_1")
        radii = np.ones(1, dtype=np.float32)
        instances = np.zeros(3,dtype=np.float32)
        coords = coords.reshape(42,3)
        # print(coords.shape)

        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)

        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)

        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, "vert_coord")
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))

        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(program, "vert_color")
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        GL.glVertexAttribDivisor(gl_colors, 1)

        rad_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
        gl_rads = GL.glGetAttribLocation(program, "vert_radius")
        GL.glEnableVertexAttribArray(gl_rads)
        GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
        GL.glVertexAttribDivisor(gl_rads, 1)

        insta_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, insta_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, instances.nbytes, instances, GL.GL_STATIC_DRAW)
        gl_insta = GL.glGetAttribLocation(program, "vert_instance")
        GL.glEnableVertexAttribArray(gl_insta)
        GL.glVertexAttribPointer(gl_insta, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))
        GL.glVertexAttribDivisor(gl_insta, 1)

        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glDisableVertexAttribArray(gl_rads)
        GL.glDisableVertexAttribArray(gl_insta)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        return vao, (coord_vbo, col_vbo, rad_vbo, insta_vbo), int(len(indexes))
 
    def draw_representation (self):
        """ Function doc """
        
        if self.instances_vao is None:
            self.instances_vao, self.instances_vbos, self.instances_elemns = self._make_gl_vao_and_vbos(self.gl_program_instances)
          
            #self.insta_rads = np.array(self.vobject.cov_radiues_list, dtype=np.float32)
            self.insta_rads = self.vobject.vdw_dot_sizes*0.07
            self.insta_col = np.array(self.vobject.colors, dtype=np.float32)
            self.insta_crd = self.vobject.frames[0]
            #for atom in 
            
            
            
            #self.insta_col = np.random.rand (5000,3).astype(np.float32)
            #self.insta_rads = np.random.rand(5000).astype(np.float32) + .2
           
            self.insta_flag_test = True
            #self.queue_draw()
        
        else:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glUseProgram(self.gl_program_instances)
            #self.load_matrices(self.gl_program_instances)
            self.glCore.load_matrices(self.gl_program_instances, self.vobject.model_mat)
            
            #self.glCore.load_fog(self.gl_program_instances)
            
            self.load_lights(self.gl_program_instances)
            
            GL.glBindVertexArray(self.instances_vao)
            if self.insta_flag_test:
                #self.set_coordinates_to_buffer()

                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.instances_vbos[1])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, self.insta_col.nbytes, self.insta_col, GL.GL_STATIC_DRAW)
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.instances_vbos[2])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, self.insta_rads.nbytes, self.insta_rads, GL.GL_STATIC_DRAW)
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.instances_vbos[3])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, self.insta_crd.nbytes, self.insta_crd, GL.GL_STATIC_DRAW)
                self.insta_flag_test = False
            
            self.insta_crd= self.glCore._safe_frame_exchange(self.vobject)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.instances_vbos[3])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, self.insta_crd.nbytes, self.insta_crd, GL.GL_STATIC_DRAW)
            
            #print (frame)
            GL.glDrawElementsInstanced(GL.GL_TRIANGLES, self.instances_elemns, GL.GL_UNSIGNED_INT, None, self.insta_crd.shape[0])
            GL.glBindVertexArray(0)
            GL.glUseProgram(0)        
            GL.glDisable(GL.GL_DEPTH_TEST)
