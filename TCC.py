from numpy import True_, arctan, cos, mod, pi, sin, sqrt, exp, tan
import streamlit as st
import time
@st.cache(suppress_st_warning=True)
def spinner():
    spinner = st.spinner('Calculando')
    with spinner:
        time.sleep(2.5)
        st.success('Feito!')
def calcula_fator_geometria(tipo_engrenagem,tipo_engrenamento,passo_diametral,larg_face,diametros_ref={},raio_pinhao=0,raio_interm=0,raio_eng=0,diametro_ref_pinhao=0):
    if tipo_engrenamento == 'Trem Simples':
        ang_pressao = st.number_input('Insira o valor do ângulo de pressão')
        coef_adendo_pinhao = st.number_input('Insira o valor do Coeficiente de Adendo do pinhão')
        coef_adendo_interm = st.number_input('Insira o valor do Coeficiente de Adendo da intermediária')
        if tipo_engrenagem == 'Dentes Retos':
            raio_curvatura1_eng1 = sqrt(((raio_pinhao)+(1+coef_adendo_pinhao)/passo_diametral)**2 - (raio_pinhao*cos(ang_pressao*pi/180))**2) - (pi/passo_diametral)*cos(ang_pressao*pi/180)
            raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180)-raio_curvatura1_eng1
            raio_curvatura1_eng2 = sqrt(((raio_interm)+(1+coef_adendo_pinhao)/passo_diametral)**2 - (raio_interm*cos(ang_pressao*pi/180))**2) - (pi/passo_diametral)*cos(ang_pressao*pi/180)
            raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180)-raio_curvatura1_eng2
            fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao)
            fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng2 + 1/raio_curvatura2_eng2)*2*raio_interm)
            return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2
        elif tipo_engrenagem == 'Dentes Helicoidais':
            coef_adendo_eng = st.number_input('Insira o valor do Coeficiente de Adendo da Engrenagem')
            angulo_helice = st.number_input('Insira o valor do Ângulo de hélice')
            fator_z_pi = sqrt((raio_pinhao+coef_adendo_pinhao)**2 - (raio_pinhao*cos(ang_pressao*pi/180))) + sqrt((raio_interm+coef_adendo_interm)**2 - (raio_interm*cos(ang_pressao*pi/180)**2)) - (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180)
            fator_z_ig= sqrt((raio_pinhao+coef_adendo_pinhao)**2 - (raio_pinhao*cos(ang_pressao*pi/180))) + sqrt((raio_eng+coef_adendo_eng)**2 - (raio_eng*cos(ang_pressao*pi/180)**2)) - (raio_interm+raio_eng)*sin(ang_pressao*pi/180)
            fator_mp_pi = passo_diametral*fator_z_pi/(pi*cos(ang_pressao*pi/180))
            fator_mp_ig = passo_diametral*fator_z_ig/(pi*cos(ang_pressao*pi/180))
            fator_mf = larg_face*passo_diametral*tan(angulo_helice*pi/180)/pi
            fator_nr_pi = fator_mp_pi%1
            fator_nr_ig = fator_mp_ig%1
            fator_na = fator_mf%1
            passo_axial = pi*cos(angulo_helice*pi/180)/(passo_diametral*sin(angulo_helice*pi/180))
            ang_pressao_normal = arctan(cos(angulo_helice*pi/180)*tan(angulo_helice*pi/180))
            angulo_helice_base = arctan(cos (angulo_helice*pi/180)*(cos (ang_pressao_normal)/cos(ang_pressao*pi/180)))
            if(fator_na < (1-fator_nr_pi)):
                l_min_pi = (fator_mp_pi*larg_face-fator_na*fator_nr_pi*passo_axial)/cos(angulo_helice_base*pi/180)
            else:
                l_min_pi = (fator_mp_pi*larg_face-(((1-fator_na)*(1-fator_nr_pi))*passo_axial))/cos(angulo_helice_base*pi/180)
            if(fator_na < (1-fator_nr_ig)):
                l_min_ig = (fator_mp_ig*larg_face-fator_na*fator_nr_ig*passo_axial)/cos(angulo_helice_base*pi/180)
            else:
                l_min_ig = (fator_mp_ig*larg_face-(((1-fator_na)*(1-fator_nr_ig))*passo_axial))/cos(angulo_helice_base*pi/180)
            fator_mn_pi = larg_face/l_min_pi
            fator_mn_ig = larg_face/l_min_ig
            if angulo_helice!=0:
                raio_curvatura1_eng1 = sqrt((0.5*((raio_pinhao+coef_adendo_pinhao)+(raio_pinhao-coef_adendo_interm))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
                raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180) - raio_pinhao
                raio_curvatura1_eng2 = sqrt((0.5*((raio_interm+coef_adendo_interm)+(raio_interm-coef_adendo_eng))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
                raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180) - raio_curvatura1_eng2
                fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao*fator_mn_pi)
                fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura2_eng1 + 1/raio_curvatura2_eng2)*2*raio_interm*fator_mn_ig)
                return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2
    else:
        ang_pressao = st.number_input('Insira o valor do ângulo de pressão')
        coef_adendo_pinhao = st.number_input('Insira o valor do Coeficiente de Adendo do Pinhão')
        if tipo_engrenagem == 'Dentes Retos':
            raio_curvatura_pinhao = sqrt(((diametros_ref[0]/2)+(1+coef_adendo_pinhao)/passo_diametral)**2 - (diametros_ref[0]/2*cos(ang_pressao*pi/180))**2) - (pi/passo_diametral)*cos(ang_pressao*pi/180)
            raio_curvatura_eng = (diametros_ref[0]/2+diametros_ref[1]/2)*sin(ang_pressao*pi/180)-raio_curvatura_pinhao
            fator_geom_sup =  cos(ang_pressao*pi/180)/((1/raio_curvatura_pinhao + 1/raio_curvatura_eng)*diametros_ref[0])
            return raio_curvatura_pinhao,raio_curvatura_eng,fator_geom_sup
        elif tipo_engrenagem == 'Dentes Helicoidais':
            coef_adendo_eng = st.number_input('Insira o valor do Coeficiente de Adendo das Engrenagens Movidas')
            fator_mp = st.number_input('Insira o valor da Razão de contato transversal')
            fator_mf = st.number_input('Insira o valor da Razão de contato axial')
            fator_nr = fator_mp%1
            fator_na = fator_mf%1
            passo_axial = st.number_input('Insira o valor do Passo axial')
            angulo_helice_base = st.number_input('Insira o valor do Ângulo de hélice de base')
            if fator_mp != 0 and fator_mf != 0 and passo_axial!= 0 and angulo_helice_base !=0:
                if(fator_na < (1-fator_nr)):
                    l_min = (fator_mp*larg_face-fator_na*fator_nr*passo_axial)/cos(angulo_helice_base*pi/180)
                else:
                    l_min = (fator_mp*larg_face-(((1-fator_na)*(1-fator_nr))*passo_axial))/cos(angulo_helice_base*pi/180)
                fator_mn = larg_face/l_min
                raio_curvatura_pinhao = sqrt((0.5*((diametros_ref[0]/2+coef_adendo_pinhao)+(diametros_ref[0]/2-coef_adendo_eng))**2)-diametros_ref[0]/2*cos(ang_pressao*pi/180)**2)
                raio_curvatura_eng = (diametros_ref[0]/2+diametros_ref[1]/2)*sin(ang_pressao*pi/180) - diametros_ref[0]/2
                fator_geom_sup =  cos(ang_pressao*pi/180)/((1/raio_curvatura_pinhao + 1/raio_curvatura_eng)*diametros_ref[0]*fator_mn)
                return raio_curvatura_pinhao,raio_curvatura_eng,fator_geom_sup

 

def calcula_resistencias(tensao_flexao_pinhao, tensao_superficie_eng1, tensao_superficie_eng2 =0, tipo_engrenamento = 'Trem Simples',tensao_flexao_interm =0, tensao_flexao_eng=0,num_engrenagens=0 ):
    st.text('Calculo das Tensões de Superfície')
    st.latex(r'''
            \sigma_c = C_p\sqrt{\frac{W_t C_a C_m C_s C_f}{FIdC_v}}
            ''')
    if(tipo_engrenamento == 'Trem Simples'):
        fator_kl = st.number_input('Forneça o fator de vida KL',step=1e-4,format='%.4f')
        temperatura_operacao = (st.number_input('Forneça a temperatura de operação em Fahrenheit'))
        if temperatura_operacao > 250:
            fator_kt = (temperatura_operacao + 460)/620
        else:
            fator_kt = 1
        fator_kr = st.selectbox('Selecione o fator Kr' , [0.85,1.00,1.25,1.50])
        coluna1,coluna2 = st.columns([4,1])
        with coluna1:
            resistencia_flexao_teorica = st.number_input('Forneça a resistência à fadiga de flexão teórica')
            resistencia_superficial_teorica = st.number_input('Forneça a resistência à fadiga superficial teórica')
        with coluna2:
            unidade_resistencia_flexao = st.radio('',('Psi','Mpa'),key=0) 
        fator_cl = st.number_input('Forneça o fator de vida de superfície Cl',step=1e-4,format='%.4f')
        fator_ch = 1
        resistencia_flexao = (resistencia_flexao_teorica*fator_kl)/(fator_kr*fator_kt)
        resistencia_superficial = (resistencia_superficial_teorica*fator_cl*fator_ch)/(fator_kt*fator_kr)
        if resistencia_superficial != 0:
            fator_seguranca_flexao_pinhao = resistencia_flexao/tensao_flexao_pinhao
            fator_seguranca_flexao_interm = resistencia_flexao/tensao_flexao_interm
            fator_seguranca_flexao_eng = resistencia_flexao/tensao_flexao_eng
            fator_seguranca_superficie_eng1 = (resistencia_superficial/tensao_superficie_eng1)**2
            fator_seguranca_superficie_eng2 = (resistencia_superficial/tensao_superficie_eng2)**2
            return resistencia_flexao,resistencia_superficial,fator_seguranca_flexao_pinhao,fator_seguranca_flexao_interm,fator_seguranca_flexao_eng,fator_seguranca_superficie_eng1,fator_seguranca_superficie_eng2, unidade_resistencia_flexao

    else:
        fator_kl = {}
        for i in range(int(num_engrenagens)):
            fator_kl[i] = st.number_input('Forneça o fator de vida KL da engrenagem {}'.format(i),step=1e-4,format='%.4f',key=i)
        temperatura_operacao = (st.number_input('Forneça a temperatura de operação em Fahrenheit'))
        if temperatura_operacao > 250:
            fator_kt = (temperatura_operacao + 460)/620
        else:
            fator_kt = 1
        fator_kr = st.selectbox('Selecione o fator Kr' , [0.85,1.00,1.25,1.50])
        col1, col2 = st.columns([3,1])
        with col1:
            resistencia_flexao_teorica = st.number_input('Forneça a resistência à fadiga de flexão não corrigida')
        with col2:
            unidade_flexao_teorica = st.radio('',('Mpa','Psi'))
        if unidade_flexao_teorica == 'Psi':
            resistencia_flexao_teorica = resistencia_flexao_teorica*6894.76
        else:
            resistencia_flexao_teorica = resistencia_flexao_teorica*10**6
        resistencia_flexao = {}
        st.write(resistencia_flexao_teorica)
        st.write(fator_kl)
        st.write(fator_kr)
        st.write(fator_kt)
        for i in range(int(num_engrenagens)):
            resistencia_flexao[i] = (resistencia_flexao_teorica*fator_kl[i])/(fator_kr*fator_kt)
        fator_cl = {}
        for i in range(int(num_engrenagens)):
            fator_cl[i] = st.number_input('Forneça o fator de vida de superfície Cl da engrenagem {}'.format(i),step=1e-4,format='%.4f',key=i)
            if i%2 != 0:
                try:
                    fator_cl[i+1] = fator_cl[i]
                    i+=1
                except:
                    pass
        fator_ch = 1
        col1, col2 = st.columns([3,1])
        with col1:
            resistencia_superficial_teorica = st.number_input('Forneça a resistência à fadiga superficial não corrigida')
        with col2:
            unidade_superficial_teorica = st.radio('',('Mpa','Psi'),key=1)
        if unidade_superficial_teorica == 'Psi':
            resistencia_superficial_teorica = resistencia_superficial_teorica*6894.76
        else:
            resistencia_superficial_teorica = resistencia_superficial_teorica*10**6
        resistencia_superficial = {}
        for i in range(int(num_engrenagens)):
            resistencia_superficial[i] = (resistencia_superficial_teorica*fator_cl[i]*fator_ch)/(fator_kt*fator_kr)
        col1,col2,col3 = st.columns([3,3,1])
        with col3:
            unidade_output = st.radio('Valores em',('Mpa','Psi'),key=2)
        if unidade_output == 'Psi':
            for i in range(int(num_engrenagens)):
                resistencia_flexao[i] = resistencia_flexao[i]/6894.7
                resistencia_superficial[i] = resistencia_superficial[i]/6894.7
                tensao_flexao_pinhao[i] = tensao_flexao_pinhao[i]/6894.7
                tensao_superficie_eng1[i] = tensao_superficie_eng1[i]/6894.7
        else:
            for i in range(int(num_engrenagens)):
                resistencia_flexao[i] = resistencia_flexao[i]*10**-6
                resistencia_superficial[i] = resistencia_superficial[i]*10**-6
                tensao_flexao_pinhao[i] = tensao_flexao_pinhao[i] *10**-6
                tensao_superficie_eng1[i] = tensao_superficie_eng1[i] *10**-6
        with col1: 
            for i in range(int(num_engrenagens)):
                st.metric('Resistência à Fadiga de Flexão corrigida Engrenagem {}'.format(i,unidade_flexao_teorica),round(resistencia_flexao[i],3))
            fator_seguranca_flexao = {}
            fator_seguranca_superficie = {}
            for i in range(0,int(len(tensao_flexao_pinhao))):
                    fator_seguranca_flexao[i] = resistencia_flexao[i]/tensao_flexao_pinhao[i]
                    fator_seguranca_superficie[i] = (resistencia_superficial[i]/tensao_superficie_eng1[i])**2
                    st.metric("F. de Segurança de Flexão da Engrenagem {}".format(i), round(fator_seguranca_flexao[i],3) )
        with col2:
            for i in range(int(num_engrenagens)):
                st.metric('Resistência à Fadiga Superfícial corrigida {} em psi'.format(i), round(resistencia_superficial[i],3))
            for i in range(0,int(len(tensao_flexao_pinhao))):
                st.metric("F. de Segurança de Superfície do {}º Engrenamento".format(i), round(fator_seguranca_superficie[i],2))
def calcula_esforcos_simples(tipo_engrenagem,tipo_engrenamento):
    st.markdown("<h1 text-align:center;>Calculo das tensões de um trem de engrenagens</h1>",True)        
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        st.image('trem-engrenagem-simples.png')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Tensão de flexão:')
        st.latex(r'''
            \sigma_b = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
            ''')
    with col2:
        st.subheader('Tensão de superfície:')
        st.latex(r'''
            \sigma_c = C_p\sqrt{\frac{W_t C_a C_m C_s C_f}{FIdC_v}}
            ''')
    st.markdown('---')
    st.subheader('Forneça os parâmetros iniciais')    
    col1, col2 = st.columns(2)
    with col1:
        dentes_pinhao = st.number_input('Quantidade de Dentes do Pinhão',step=1)
        dentes_interm = st.number_input('Quantidade de Dentes da Engrenagem Intemediária',step=1)
        larg_face = st.number_input('Insira o valor da largura de face',step=.001,format='%.3f')
    with col2:
        passo_diametral = st.number_input('Insira o valor do passo diametral Pd:',step=.1)
        dentes_eng = st.number_input('Quantidade de Dentes da Engrenagem',step=1)  
        unidade_medida_largface = st.radio('Unidade de medida',('In', 'mm'))  
    if unidade_medida_largface == 'mm':
        larg_face = larg_face*0.0393701
    if passo_diametral !=0 and dentes_pinhao !=0 and dentes_interm !=0 and dentes_eng !=0:
        diametro_ref_pinhao = dentes_pinhao/passo_diametral 
        diametro_ref_interm = dentes_interm/passo_diametral
        diametro_ref_eng = dentes_eng/passo_diametral
        c1,c2,c3,c4,c5,c6 = st.columns([1,2,1,2,1,2])
        with c1:
            st.latex(r'''d_p =''')
        with c2:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_pinhao,2)),True)
        with c3:
            st.latex(r'''d_i =''')
        with c4:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_interm,2)),True)
        with c5:
            st.latex(r'''d_g =''')
        with c6:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_eng,2)),True)    
        vel_pinhao = st.number_input('Velocidade angular do pinhão em RPM',step=.5)
        fator_aplicacao = st.selectbox('Selecione o Fator de Aplicação KA',
        [1.00,1.25,1.5,1.75,2.00,2.25])
        fator_distribuicao = st.selectbox('Selecione o Fator de Distribuição de Carga KM',
        [1.6,1.7,1.8,2.0])
        indice_qualidade = st.number_input('Insira o valor do índice de qualidade Qv',step=.1)
        if indice_qualidade!=0 and fator_distribuicao!=0 and vel_pinhao!=0 and fator_aplicacao!=0:
            vel_linha_ref = diametro_ref_pinhao*vel_pinhao*2*pi/(2*12)
            B = ((12-indice_qualidade)**(2/3))/4
            A = 50+56*(1-B)
            fator_dinamico =(A/(A+vel_linha_ref**(1/2)))**B  
            st.metric('Fator dinâmico Kv',round(fator_dinamico,2))
        fator_tamanho = st.selectbox('Selecione o valor do Fator de Tamanho Ks',
        [1.00,1.25,1.50])
        espessura_borda = st.number_input('Forneça a espessura da borda (tR), caso existente')
        if espessura_borda > 0:
            profundidade_dente = st.number_input('Forneça a Profundidade do dente')
            try:
                razao_recuo = espessura_borda/profundidade_dente
                if razao_recuo >= 0.5 and razao_recuo <= 1.2:
                    fator_borda = -2*razao_recuo + 3.4
                elif razao_recuo >1.2:
                    fator_borda = 1
                else:
                    fator_borda = 1
            except:
                fator_borda = 1 
        else:
            fator_borda = 1       
        fator_ciclocarga = 1
        fator_ciclocarga_interm = 1.42
        colu1,colu2,colu3 = st.columns(3)
        with colu1:
            fator_geometria_flexao_pinhao = st.number_input('Determine o fator de flexão do Pinhão (J)')
        with colu2:
            fator_geometria_flexao_interm = st.number_input('Determine o fator de flexão da Engrenagem Intermediária (J)')
        with colu3:
            fator_geometria_flexao_eng = st.number_input('Determine o fator de flexão da Engrenagem Final (J)')
        coluna1,coluna2 = st.columns(2)
        with coluna1:
            carga_axial = st.number_input('Forneça a Carga Aplicada',step=.1)
        with coluna2:
            unidade_carga = st.radio(label = '',options=('lb','N'))
        if unidade_carga == 'N':
            carga_axial = carga_axial*4.448222
        if (carga_axial !=0) and (fator_geometria_flexao_pinhao != 0) and (fator_geometria_flexao_interm != 0) and (fator_geometria_flexao_eng != 0):
            spinner()  
            tensao_flexao_pinhao = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face*fator_geometria_flexao_pinhao*fator_dinamico)
            tensao_flexao_interm = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga_interm/(larg_face*fator_geometria_flexao_interm*fator_dinamico)
            tensao_flexao_eng = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face*fator_geometria_flexao_eng*fator_dinamico) 
            col1,col2 = st.columns(2)
            with col1:
                st.latex(r'''
                \sigma = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
                ''')
            with col2:
                unidade_tensao_flexao = st.radio('',('Psi','Mpa')) 
            if unidade_tensao_flexao == 'Mpa':
                tensao_flexao_pinhao = tensao_flexao_pinhao *6894.76/10**6
                tensao_flexao_interm = tensao_flexao_interm *6894.76/10**6
                tensao_flexao_eng = tensao_flexao_eng *6894.76/10**6
            c1,c2,c3 = st.columns(3)
            with c1:
                st.metric('Tensão de Flexão no Pinhão', round(tensao_flexao_pinhao,2), unidade_tensao_flexao)
            with c2:    
                st.metric('Tensão de Flexão na Intermediária',round(tensao_flexao_interm,2),unidade_tensao_flexao)
            with c3:
                st.metric('Tensão de Flexão na Engrenagem',round(tensao_flexao_eng,2),unidade_tensao_flexao)    
            st.text('Calculo do Coeficiente Elástico')
            st.latex(r'''
                        C_p = \sqrt{\frac{1}{pi[(\frac{1-v_g²}{E_p}+\frac{(1-v_g²)}{E_g})]}}
                        ''')
            col1, col2,col3 = st.columns([2,2,1])
            with col1:
                mod_elast_pinhao = float(st.number_input('Insira o Módulo de Elasticidade do pinhão (x10⁶)'))
                poisson_pinhao = float(st.number_input('Insira o Coeficiente de Poisson do pinhão'))
            with col2:    
                mod_elast_eng = float(st.number_input('Insira o Módulo de Elasticidade da engrenagem (x10⁶)'))
                poisson_eng = float(st.number_input('Insira o Coeficiente de Poisson da engrenagem') )
            with col3:
                unidade_cp = st.radio('',('Mpa','Mpsi'))
            if poisson_eng !=0 and poisson_pinhao !=0 and mod_elast_eng != 0 and mod_elast_pinhao !=0 :
                coef_elastico =  (1/(pi*(((1-poisson_pinhao**2)/(mod_elast_pinhao*10**6))+((1-poisson_eng**2)/(mod_elast_eng*10**6)))))**(1/2)
                if unidade_cp == 'Mpa':
                    st.metric('Cp (em √Mpa) = ',round(coef_elastico,2))
                else:
                    st.metric('Cp (em √psi) = ',round(coef_elastico,2))
                raio_pinhao = diametro_ref_pinhao/2
                raio_interm = (dentes_interm/passo_diametral)/2
                raio_eng = (dentes_eng/passo_diametral)/2
                fator_acab_superficial = 1
                try:
                    if fator_acab_superficial == 1:
                        raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2 = calcula_fator_geometria(tipo_engrenagem,tipo_engrenamento,raio_pinhao=raio_pinhao,passo_diametral=passo_diametral,raio_interm=raio_interm,raio_eng=raio_eng,diametro_ref_pinhao=diametro_ref_pinhao,larg_face=larg_face)
                        tensao_superficie_eng1 = 0
                        tensao_superficie_eng1 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng1*diametro_ref_pinhao*fator_dinamico))
                        tensao_superficie_eng2 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng2*raio_interm*2*fator_dinamico))
                        resist_flexao_corrigida,resist_superficial_corrigida,nb_pinhao,nb_interm,nb_eng,ns_1,ns_2,unidade_resistencia_flexao=calcula_resistencias(tensao_flexao_pinhao, tensao_flexao_interm=tensao_flexao_interm, tensao_flexao_eng=tensao_flexao_eng ,tensao_superficie_eng1=tensao_superficie_eng1, tensao_superficie_eng2=tensao_superficie_eng2)
                        if raio_curvatura1_eng1 != 0:
                            if unidade_resistencia_flexao == 'Mpa':
                                tensao_superficie_eng1 = tensao_superficie_eng1 * 6894.76 
                                tensao_superficie_eng2 = tensao_superficie_eng2 * 6894.76 
                            c1,c2 = st.columns(2)
                            with c1:
                                st.metric("P1 Engrenamento Pinhão-Intermediária", round(raio_curvatura1_eng1,4))
                                st.metric("P2 Engrenamento Pinhão-Intermediária", round(raio_curvatura2_eng1,4))
                                st.metric('Fator I Engrenamento Pinhão-Intermediária', round(fator_geom_sup_eng1,4))
                                st.metric("Tensão de Superfície Pinhão-Intermediária", round(tensao_superficie_eng1,4),unidade_resistencia_flexao)
                            with c2:
                                st.metric("P1 Engrenamento Intermediária-Engrenagem", round(raio_curvatura1_eng2,4))
                                st.metric("P2 Engrenamento Intermediária-Engrenagem", round(raio_curvatura2_eng2,4))
                                st.metric('Fator I Engrenamento Intermediária-Engrenagem', round(fator_geom_sup_eng2,4))
                                st.metric('Tensão de Superfície Intermediária-Engrenagem', round(tensao_superficie_eng2,4),unidade_resistencia_flexao)
                        col1,col2 = st.columns(2)
                        if resist_flexao_corrigida != 0:
                            with col1: 
                                st.metric('Resistência à Fadiga de Flexão corrigida',round(resist_flexao_corrigida,4),unidade_resistencia_flexao)
                                st.metric("Fator de Segurança de Flexão do Pinhão", round(nb_pinhao,2) )
                                st.metric("Fator de Segurança de Flexão da Intermediária", round(nb_interm,2) )
                                st.metric('Fator de Segurança de Flexão da Engrenagem', round(nb_eng,2) )
                            with col2:
                                st.metric('Resistência à Fadiga Superfícial corrigida', round(resist_superficial_corrigida,4),unidade_resistencia_flexao)
                                st.metric("Fator de Segurança de Superfície do 1º Engrenamento", round(ns_1,2))
                                st.metric("Fator de Segurança de Superfície do 2º Engrenamento", round(ns_2,2))
                except:
                    pass
def calcula_esforcos_composto(tipo_engrenagem,tipo_engrenamento):
    st.markdown("<h1 text-align:center;>Calculo das tensões de um trem de engrenagens</h1>",True)        
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        st.image('trem-engrenagem-composto.png')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Tensão de flexão:')
        st.latex(r'''
            \sigma_b = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
            ''')
    with col2:
        st.subheader('Tensão de superfície:')
        st.latex(r'''
            \sigma_c = C_p\sqrt{\frac{W_t C_a C_m C_s C_f}{FIdC_v}}
            ''')
    st.markdown('---')
    st.subheader('Forneça os parâmetros iniciais')    
    col1, col2 = st.columns(2)
    with col1:
        numero_estagios = st.number_input('Insira o número de estágios',format='%i',step=1 )
        numero_engrenagens = 2*numero_estagios
        razao_engrenamento = st.number_input('Determine a razão de engrenamento de cada engrenamento')
        engrenagens = {}
    with col2:
        passo_diametral = st.number_input('Insira o valor do passo diametral:',step=.1)
        engrenagens[0] = st.number_input('Determine o número de dentes da engrenagem 0',format=='%i',step=1)
        if numero_estagios!= 0:
            for i in range(2,int(numero_engrenagens),2):
                engrenagens[i] = engrenagens[0]                    
            for i in range(1,int(numero_engrenagens),2):
                engrenagens[i] = engrenagens[0]*razao_engrenamento
    if passo_diametral !=0 and numero_estagios !=0 and razao_engrenamento !=0 and engrenagens[0] !=0:
        col1,col2 = st.columns(2)
        with col1:
            larg_face = st.number_input('Insira o valor da largura de face',step=.001,format='%.3f')
        with col2:    
            unidade = st.radio(label='Unidade',options=('mm','In')) 
        if unidade == 'In':
            larg_face = larg_face*25.4*10**-3
        else:
            larg_face = larg_face*10**-3
        diametros_ref = {}
        for i in range (0,int(numero_engrenagens)):
            diametros_ref[i] = engrenagens[i]/passo_diametral
        velocidades = {}
        velocidades_linha_ref = {}
        velocidades[0] = st.number_input('Velocidade angular do pinhão em RPM',step=.5)
        fator_aplicacao = st.selectbox('Selecione o Fator de Aplicação KA',
        [1.00,1.25,1.5,1.75,2.00,2.25])
        fator_distribuicao = st.selectbox('Selecione o Fator de Distribuição de Carga KM',
        [1.6,1.7,1.8,2.0])
        indice_qualidade = st.number_input('Insira o valor do índice de qualidade Qv',step=.1)
        fator_tamanho = st.selectbox('Selecione o valor do Fator de Tamanho Ks',[1.00,1.25,1.50])
        espessura_borda = st.number_input('Forneça a espessura da borda (tR), caso existente')
        for i in range(1,int(numero_engrenagens),2):
            velocidades[i] = velocidades[i-1]/razao_engrenamento
            velocidades[i+1] = velocidades[i]
        for i in range(0,int(numero_engrenagens)):
            velocidades_linha_ref[i] = velocidades[i]*2*pi*diametros_ref[i]/(60*2)
        B = ((12-indice_qualidade)**(2/3))/4
        A = 50+56*(1-B)
        fator_dinamico = {}
        velocidades_linha_ref_ft = {}
        for i in range(0,int(numero_engrenagens)):
            velocidades_linha_ref_ft[i] = velocidades_linha_ref[i]*5
            fator_dinamico[i] = (A/(A+velocidades_linha_ref_ft[i]**(1/2)))**B
        if espessura_borda > 0:
            profundidade_dente = st.number_input('Forneça a Profundidade do dente')
            try:
                razao_recuo = espessura_borda/profundidade_dente
                if razao_recuo >= 0.5 and razao_recuo <= 1.2:
                    fator_borda = -2*razao_recuo + 3.4
                elif razao_recuo >1.2:
                    fator_borda = 1
            except:
                pass
        else:
            fator_borda = 1
        fator_ciclocarga = 1
        fator_geometria = {}
        fator_geometria[0] = st.number_input('Insira o fator de geometria do Pinhão')
        fator_geometria[1] = st.number_input('Insira o fator de geometria da engrenagem')
        for i in range(2,int(numero_engrenagens)-1,2):
            fator_geometria[i] = fator_geometria[0]
        for i in range(3,int(numero_engrenagens),2):
            fator_geometria[i] = fator_geometria[1]
        potencia = st.number_input('Forneça a Potencia Aplicada em Watts',step=.1)
        modulo = 25.4 * 10**-3 /passo_diametral
        carga_axial = {}
        for i in range(0,int(numero_engrenagens)-1,2):
            carga_axial[i] = potencia /(velocidades_linha_ref[i]/39.3701)
            carga_axial[i+1] = carga_axial[i]
        if (potencia !=0) :
            spinner()  
            st.latex(r'''
            \sigma = \frac{W_t K_a K_m K_s K_b K_I}{FJK_v}
            ''')
            tensao_flexao = {}
            for i in range(0,int(numero_engrenagens)):
                tensao_flexao[i] = carga_axial[i]*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face*modulo*fator_geometria[i]*fator_dinamico[i])
                st.metric('Tensão de flexão na Engrenagem {} (Mpa)'.format(i),round(tensao_flexao[i]*10**-6,3))
            st.text('Calculo do Coeficiente Elástico')
            st.latex(r'''
                        C_p = \sqrt{\frac{1}{pi[(\frac{1-v_g²}{E_p}+\frac{(1-v_g²)}{E_g})]}}
                        ''')
            col1, col2 = st.columns([3,1])
            with col1:
                poisson_pinhao = float(st.number_input('Insira o Coeficiente de Poisson do pinhão'))
                mod_elast_pinhao = float(st.number_input('Insira o Módulo de Elasticidade do pinhão'))
                poisson_eng = float(st.number_input('Insira o Coeficiente de Poisson da engrenagem') )
                mod_elast_eng = float(st.number_input('Insira o Módulo de Elasticidade da engrenagem '))
                mod_elast_pinhao = mod_elast_pinhao*10**6
                mod_elast_eng = mod_elast_eng*10**6
            with col2:    
                unidade = st.radio('Unidade',('Mpa','psi'))
                if unidade == 'psi':
                    mod_elast_eng = mod_elast_eng*6894.76
                    mod_elast_pinhao = mod_elast_pinhao*6894.76
            if poisson_eng !=0 and poisson_pinhao !=0 and mod_elast_eng != 0 and mod_elast_pinhao !=0 :
                coef_elastico =  (1/(pi*(((1-poisson_pinhao**2)/(mod_elast_pinhao))+((1-poisson_eng**2)/(mod_elast_eng)))))**(1/2)
                if unidade == 'Mpa':
                    st.metric('Cp (em √Mpa) = ',round(coef_elastico,2))
                else:
                    st.metric('Cp (em √psi) = ',round(coef_elastico,2))
                fator_acab_superficial = 1
                raio_curvatura_pinhao,raio_curvatura_eng,fator_geom_sup = calcula_fator_geometria(tipo_engrenagem=tipo_engrenagem,tipo_engrenamento=tipo_engrenamento,diametros_ref=diametros_ref,passo_diametral = passo_diametral,larg_face = larg_face)
                tensao_superficie = {}
                for i in range (0,int(numero_engrenagens)):
                    diametros_ref[i] = engrenagens[i]/passo_diametral * 25.4 * 10**-3
                for i in range(0,int(numero_engrenagens),2):
                    tensao_superficie[i] = coef_elastico*sqrt((carga_axial[i]*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup*diametros_ref[i]*fator_dinamico[i]))
                for i in range(1,int(numero_engrenagens),2):
                    tensao_superficie[i] = tensao_superficie[i-1]
                for i in range(0,int(numero_engrenagens),2):
                    st.metric("Tensão de superfície Engrenamento" + str(i) + str(i+1) + ' (MPA)', round(tensao_superficie[i]/10**6,3))  
                calcula_resistencias(tensao_flexao,tensao_superficie,tipo_engrenamento=tipo_engrenamento,num_engrenagens=numero_engrenagens)
                
def main():
    tipo_engrenagem = st.sidebar.selectbox('Selecione o tipo de engrenagem',('Dentes Retos', 'Dentes Helicoidais'))
    tipo_engrenamento = st.sidebar.selectbox('Selecione o tipo de engrenamento',('Trem Simples','Trem Composto'))
    if tipo_engrenamento == 'Trem Simples':
        calcula_esforcos_simples(tipo_engrenagem,tipo_engrenamento)
    else:
        calcula_esforcos_composto(tipo_engrenagem,tipo_engrenamento)


if __name__ == "__main__":
    main()

