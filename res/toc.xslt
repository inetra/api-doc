<?xml version='1.0' encoding='utf-8'?>

<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	version="1.0">

	<xsl:output method='xml' version="1.0" encoding='utf-8' doctype-public="-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" doctype-system="http://www.w3.org/TR/MathML2/dtd/xhtml-math11-f.dtd" indent="no"/>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="*[@id='']">
		<xsl:copy>
			<xsl:apply-templates select="@*"/>
			<xsl:attribute name="id">h<xsl:apply-templates select="." mode="tocNumber"/></xsl:attribute>
			<xsl:apply-templates/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="a">
		<xsl:copy>
			<xsl:apply-templates select="@*"/>
			<xsl:attribute name="target">_top</xsl:attribute>
			<xsl:apply-templates/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="body">
		<xsl:copy>
			<h1>
				<xsl:value-of select="/html/head/title"/>
			</h1>
			<xsl:variable name="document.info">
				<xsl:apply-templates select="/html/head/meta" mode="InetraDocumentInfo"/>
			</xsl:variable>
			<xsl:if test="$document.info != ''">
				<h2>Статус документа</h2>
				<div class="document-info">
					<ul>
						<xsl:apply-templates select="/html/head/meta" mode="InetraDocumentInfo"/>
					</ul>
				</div>
			</xsl:if>
			<h2>Оглавление</h2>
			<div>
				<xsl:attribute name="class">toc</xsl:attribute>
				<ul>
					<xsl:apply-templates select="h1" mode="printToc"/>
				</ul>
			</div>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="meta" mode="InetraDocumentInfo">
		<xsl:variable name="text">
			<xsl:choose>
				<xsl:when test="@name='version'">
					<xsl:text>Версия документа</xsl:text>
				</xsl:when>
				<xsl:when test="@name='server-version'">
					<xsl:text>Поддерживаемые версии</xsl:text>
				</xsl:when>
				<xsl:when test="@name='status'">
					<xsl:text>Статус версии</xsl:text>
				</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:if test="$text != ''">
			<li>
				<xsl:value-of select="$text"/>: <xsl:value-of select="@content"/>
			</li>
		</xsl:if>
	</xsl:template>

	<xsl:template match="meta[@name='jira-ticket']" mode="InetraDocumentInfo">
		<xsl:variable name="ticket" select="@content"/>
		<li>
			<xsl:text>Тикет на разработку: </xsl:text>
			<a href="http://drug/ijira/browse/{$ticket}">
				<xsl:value-of select="$ticket"/>
			</a>
		</li>
	</xsl:template>

	<xsl:template mode="tocNumber" match="*">
		<xsl:variable name="currentHeadingNumber" select="number(substring(local-name(), 2))"/>
		<xsl:variable name="previousLevelNumber" select="number(substring(local-name(preceding::*[number(substring(local-name(), 2)) &lt; $currentHeadingNumber][1]), 2))"/>

		<xsl:apply-templates mode="tocNumber" select="preceding::*[number(substring(local-name(), 2)) = $previousLevelNumber][1]"/>
		<xsl:value-of select="count(preceding::*[number(substring(local-name(), 2)) = $currentHeadingNumber]) - count(preceding::*[number(substring(local-name(), 2)) = $previousLevelNumber][1]/preceding::*[number(substring(local-name(), 2)) = $currentHeadingNumber]) + 1"/>
		<xsl:text>.</xsl:text>
	</xsl:template>

    <xsl:template match="*" mode="printToc">
		<xsl:variable name="currentHeadingNumber" select="number(substring(local-name(), 2))"/>
		<xsl:variable name="nextHeadingNumber" select="number(substring(name(following::*[string(number(substring(local-name(), 2))) != 'NaN'][1]), 2))"/>
		<xsl:variable name="tocNumber"><xsl:apply-templates select="." mode="tocNumber"/></xsl:variable>
		<xsl:variable name="href">
			<xsl:choose>
				<xsl:when test="not(@id) or @id=''">
					<xsl:text>h</xsl:text><xsl:value-of select="$tocNumber"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="@id"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<li>
			<a href="#{$href}">
				<xsl:value-of select="$tocNumber"/><xsl:text>&#160;</xsl:text>
				<xsl:value-of select="."/>
			</a>
			<xsl:if test="$nextHeadingNumber &gt; $currentHeadingNumber">
				<ul>
					<xsl:variable name="nextLevelCount" select="count(following::*[local-name() = concat('h', $currentHeadingNumber)][1]/preceding::*[local-name() = concat('h', $nextHeadingNumber)]) - count(preceding::*[local-name() = concat('h', $nextHeadingNumber)])"/>
					<xsl:apply-templates mode="printToc" select="following::*[local-name() = concat('h', $nextHeadingNumber)][(position() &lt; ($nextLevelCount + 1)) or ($nextLevelCount &lt; 1)]"/>
				</ul>
			</xsl:if>
		</li>
	</xsl:template>

</xsl:stylesheet>
